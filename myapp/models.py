from django.db import models

class Extrinsic(models.Model):
    extrinsic_address = models.CharField(max_length=100, null = True)
    extrinsic_hash = models.CharField(max_length=100, null = True)
    extrinsic_netuid = models.IntegerField(null = True)
    extrinsic_block = models.IntegerField(null = True)
    extrinsic_idx = models.CharField(max_length=10, null = True)
    block_hash = models.CharField(max_length=100, null = True)

    def __str__(self):
        return f"{self.extrinsic_address} - {self.extrinsic_hash}"