from pathlib import Path
from flask import abort, g
from flask import current_app as app

import boto3
from boto3.dynamodb.types import TypeDeserializer
from boto3.dynamodb.conditions import Key


dynamo_config = {
    'region_name': app.config['DYNAMODB_REGION']
}

if 'DYNAMODB_ENDPOINT' in app.config:
    dynamo_config['endpoint_url'] = app.config['DYNAMODB_ENDPOINT']

client = boto3.client('dynamodb', **dynamo_config)
resource = boto3.resource('dynamodb', **dynamo_config)



class Nota:

    table = 'notas'
    _pk_field = 'codigo'
    deserializer = TypeDeserializer()
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
        return Nota(**document['Item'])
    
    def save(self):
        Nota.table.put_item(Item=self.__dict__)
        return self
    
    def delete(self):
        Nota.table.delete_item(Key={Nota._pk_field: self.codigo})
        return self
    



