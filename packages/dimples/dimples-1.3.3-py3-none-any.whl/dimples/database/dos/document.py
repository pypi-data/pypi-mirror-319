# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2022 Albert Moky
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

from typing import Optional, List

from dimsdk import TransportableData
from dimsdk import ID, Document, DocumentUtils

from ...utils import template_replace
from ...common import DocumentDBI

from .base import Storage


class DocumentStorage(Storage, DocumentDBI):
    """
        Document for Entities (User/Group)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        file path: '.dim/public/{ADDRESS}/documents.js'
    """
    docs_path = '{PUBLIC}/{ADDRESS}/documents.js'

    def show_info(self):
        path = self.public_path(self.docs_path)
        print('!!!      documents path: %s' % path)

    def __docs_path(self, identifier: ID) -> str:
        path = self.public_path(self.docs_path)
        return template_replace(path, key='ADDRESS', value=str(identifier.address))

    async def save_documents(self, documents: List[Document], identifier: ID) -> bool:
        """ save documents into file """
        path = self.__docs_path(identifier=identifier)
        self.info(msg='Saving %d document(s) into: %s' % (len(documents), path))
        array = []
        for doc in documents:
            assert doc.identifier == identifier, 'document ID not matched: %s, %s' % (identifier, doc)
            array.append(doc.dictionary)
        return await self.write_json(container=array, path=path)

    async def load_documents(self, identifier: ID) -> Optional[List[Document]]:
        """ load documents from file """
        path = self.__docs_path(identifier=identifier)
        self.info(msg='Loading documents from: %s' % path)
        array = await self.read_json(path=path)
        if array is None:
            # file not found
            self.warning(msg='document file not found: %s' % path)
            return None
        documents = []
        for info in array:
            doc = parse_document(dictionary=info, identifier=identifier)
            assert doc is not None, 'document error: %s, %s' % (identifier, info)
            documents.append(doc)
        self.info(msg='Loaded %d documents from: %s' % (len(documents), path))
        return documents

    #
    #   Document DBI
    #

    # Override
    async def save_document(self, document: Document) -> bool:
        """ save document into file """
        identifier = document.identifier
        doc_type = document.type
        # check old documents
        all_documents = await self.get_documents(identifier=identifier)
        old = DocumentUtils.last_document(all_documents, doc_type)
        if old is None and doc_type == Document.VISA:
            old = DocumentUtils.last_document(all_documents, 'profile')
        if old is not None:
            if DocumentUtils.is_expired(document, old):
                self.warning(msg='drop expired document: %s' % identifier)
                return False
            all_documents.remove(old)
        # append it
        all_documents.append(document)
        return await self.save_documents(documents=all_documents, identifier=identifier)

    # Override
    async def get_documents(self, identifier: ID) -> List[Document]:
        """ load documents from file """
        docs = await self.load_documents(identifier=identifier)
        return [] if docs is None else docs


def parse_document(dictionary: dict, identifier: ID = None, doc_type: str = '*') -> Optional[Document]:
    # check document ID
    doc_id = ID.parse(identifier=dictionary.get('ID'))
    assert doc_id is not None, 'document error: %s' % dictionary
    if identifier is None:
        identifier = doc_id
    else:
        assert identifier == doc_id, 'document ID not match: %s, %s' % (identifier, doc_id)
    # check document type
    doc_ty = dictionary.get('type')
    if doc_ty is not None:
        doc_type = doc_ty
    # check document data
    data = dictionary.get('data')
    if data is None:
        # compatible with v1.0
        data = dictionary.get('profile')
    # check document signature
    signature = dictionary.get('signature')
    if data is None or signature is None:
        raise ValueError('document error: %s' % dictionary)
    ted = TransportableData.parse(signature)
    doc = Document.create(doc_type=doc_type, identifier=identifier, data=data, signature=ted)
    for key in dictionary:
        if key == 'ID' or key == 'data' or key == 'signature':
            continue
        doc[key] = dictionary[key]
    return doc
