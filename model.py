from pathlib import Path
from flask import abort, g, current_app

import boto3
from boto3.dynamodb.types import TypeDeserializer
from boto3.dynamodb.conditions import Key




class Nota:

    table = 'notas'
    _pk_field = 'codigo'
    deserializer = TypeDeserializer()
    client = boto3.client('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2')
    resource = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2')
    table = resource.Table('notas')

    def __init__(self, codigo, titulo, texto, **kwargs):
        self.codigo = codigo
        self.titulo = titulo
        self.texto = texto
        self.__dict__.update(kwargs)

    def get(pk):
        document = Nota.table.get_item(Key={Nota._pk_field: pk})
        if 'Item' not in document:
            return None
        #dd = {k: Nota.deserializer.deserialize(v) for k, v in document['Item'].items()}
        return Nota(**document['Item'])
    
    def save(self):
        Nota.table.put_item(Item=self.__dict__)
        return self
    
    def delete(self):
        Nota.table.delete_item(Key={Nota._pk_field: self.codigo})
        return self
    



