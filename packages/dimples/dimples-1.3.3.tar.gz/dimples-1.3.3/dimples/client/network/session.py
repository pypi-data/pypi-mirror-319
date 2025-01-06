# -*- coding: utf-8 -*-
#
#   DIM-SDK : Decentralized Instant Messaging Software Development Kit
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

"""
    Session Server
    ~~~~~~~~~~~~~~

    for login user
"""

import traceback
from typing import Optional, List

from dimsdk import Station

from startrek import Porter, PorterStatus
from startrek import Arrival

from ...utils import StateDelegate
from ...utils import Daemon, Runner
from ...common import SessionDBI
from ...conn import BaseSession
from ...conn import MTPStreamArrival

from .state import StateMachine, SessionState


class ClientSession(BaseSession):
    """
        Session for Connection
        ~~~~~~~~~~~~~~~~~~~~~~

        'key' - Session Key
                A random string generated by station.
                It will be set after handshake success.

        'ID' - Local User ID
                It will be set before connecting to remote station.
                When it's empty, the session state would be 'Default'.

        'active' - Session Status
                It will be set to True after connected to remote station.
                When connection broken, it will be set to False.
                Only send message when it's True.

        'station' - Remote Station
                Station with remote IP & port, its ID will be set
                when first handshake responded, and we can trust
                all messages from this ID after that.
    """

    def __init__(self, station: Station, database: SessionDBI):
        super().__init__(remote=(station.host, station.port), sock=None, database=database)
        self.__station = station
        # session key
        self.__key: Optional[str] = None
        self.__accepted = False
        # state machine
        self.__fsm = StateMachine(session=self)
        # background thread to drive gate & hub processing
        self.__daemon = Daemon(target=self)

    @property
    def station(self) -> Station:
        return self.__station

    @property
    def session_key(self) -> Optional[str]:
        return self.__key

    @session_key.setter
    def session_key(self, key: str):
        self.__key = key

    @property
    def accepted(self) -> bool:
        return self.__accepted

    @accepted.setter
    def accepted(self, flag: bool):
        self.__accepted = flag

    @property
    def ready(self) -> bool:
        if self.active and self.accepted:
            return self.identifier is not None and self.session_key is not None

    @property
    def fsm(self) -> StateMachine:
        return self.__fsm

    @property
    def state(self) -> SessionState:
        ss = self.fsm.current_state
        if ss is None:
            ss = self.fsm.default_state
        assert isinstance(ss, SessionState), 'session state error: %s' % ss
        return ss

    # Override
    def set_active(self, active: bool, when: float = None) -> bool:
        if not active:
            self.__accepted = False
        return super().set_active(active=active, when=when)

    def start(self, delegate: StateDelegate):
        if self.running:
            # await self.stop()
            return False
        # start state machine
        fsm = self.fsm
        fsm.delegate = delegate
        Runner.async_task(coro=fsm.start())
        # start an async task for this session
        self.__daemon.start()
        # await self.run()

    # Override
    async def stop(self):
        # 1. mark this session to stopped
        await super().stop()
        # 2. stop state machine
        await self.fsm.stop()
        # 3. waiting for the session to stopped
        await Runner.sleep(seconds=self.interval * 2)
        # 4. cancel the async task
        self.__daemon.stop()

    # Override
    async def setup(self):
        await super().setup()
        self.set_active(active=True)

    # Override
    async def finish(self):
        self.set_active(active=False)
        await super().finish()

    #
    #   Docker Delegate
    #

    # Override
    async def porter_status_changed(self, previous: PorterStatus, current: PorterStatus, porter: Porter):
        # await super().porter_status_changed(previous=previous, current=current, porter=porter)
        if current is None or current == PorterStatus.ERROR:
            # connection error or session finished
            self.set_active(active=False)
            self.warning(msg='connection lost, waiting for reconnecting: %s' % porter)
            # TODO: clear session ID and handshake again
        elif current == PorterStatus.READY:
            # connected/reconnected
            self.set_active(active=True)

    # Override
    async def porter_received(self, ship: Arrival, porter: Porter):
        # await super().porter_received(ship=ship, porter=porter)
        all_responses = []
        messenger = self.messenger
        # 1. get data packages from arrival ship's payload
        packages = get_data_packages(ship=ship)
        for pack in packages:
            try:
                # 2. process each data package
                responses = await messenger.process_package(data=pack)
                for res in responses:
                    if len(res) == 0:
                        # should not happen
                        continue
                    all_responses.append(res)
            except Exception as error:
                source = porter.remote_address
                self.error(msg='parse message failed (%s): %s, %s' % (source, error, pack))
                traceback.print_exc()
                # from dimsdk import TextContent
                # return TextContent.new(text='parse message failed: %s' % error)
        gate = self.gate
        source = porter.remote_address
        destination = porter.local_address
        # 3. send responses separately
        for res in all_responses:
            await gate.send_response(payload=res, ship=ship, remote=source, local=destination)


def get_data_packages(ship: Arrival) -> List[bytes]:
    assert isinstance(ship, MTPStreamArrival), 'arrival ship error: %s' % ship
    payload = ship.payload
    # check payload
    if payload is None or len(payload) == 0:
        return []
    elif payload.startswith(b'{'):
        # JsON in lines
        return payload.splitlines()
    else:
        # TODO: other format?
        return [payload]
