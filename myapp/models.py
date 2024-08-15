from django.db import models

class Block(models.Model):
    block_id = models.IntegerField(unique = True)
    block_hash = models.CharField(max_length=100, unique=True)
    parentHash = models.CharField(max_length=100)
    stateRoot = models.CharField(max_length=100)
    extrinsicsRoot = models.CharField(max_length=100)
    # digest = models.JSONField(null = True)
    timestamp = models.DateTimeField(null=True)

    def __str__(self):
        return f"Block {self.block_number} - {self.block_hash}"

class Call(models.Model):
    call_index = models.CharField(max_length= 12, unique = True)
    call_function = models.CharField(max_length= 30, null = True)
    call_module = models.CharField(max_length= 30, null = True)

class Extrinsic(models.Model):
    netuid = models.IntegerField(null = True)  
    hash = models.CharField(max_length=64, unique=True)  
    address = models.CharField(max_length=255, null = True)  
    block = models.ForeignKey(Block, on_delete=models.CASCADE, to_field='block_id', related_name='extrinsics')
    idx = models.CharField(max_length= 12, null = True)  
    signature = models.JSONField(null = True)  
    tip = models.IntegerField(null = True)  
    nonce = models.IntegerField(null = True)  
    era = models.CharField(max_length=10, null = True)  
    call_index = models.ForeignKey(Call, on_delete=models.CASCADE, to_field='call_index', related_name='extrinsics')
    call_args = models.JSONField(null = True)  
    result = models.CharField(max_length=20, null = True)  
    events = models.JSONField(null = True)  
    def __str__(self):
        return f'Extrinsic {self.hash} at block {self.block_number}'
    


# python3 manage.py makemigrations myapp
# python3 manage.py migrate 
# python3 manage.py graph_models myapp -o myapp_models.svg