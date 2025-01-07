from typing import Type
from enum import StrEnum
from rid_lib import RID
from .cache import Cache, CacheBundle
from .manifest import Manifest


class ActionType(StrEnum):
    dereference = "dereference"

class Effector:
    def __init__(self, cache: Cache | None = None):
        self.cache = cache
        self._action_table = {}
        
    def __getattr__(self, action_type):
        def execute(rid: RID, *args, **kwargs):
            return self.execute(action_type, rid, *args, **kwargs)
        return execute
        
    def register(
        self, 
        action_type: ActionType, 
        rid_type: Type[RID] | str | tuple[Type[RID] | str]
    ):
        def decorator(func):
            if isinstance(rid_type, (list, tuple)):
                rid_types = rid_type
            else:
                rid_types = (rid_type,)
            
            for _rid_type in rid_types:
                if isinstance(_rid_type, type) and issubclass(_rid_type, RID):
                    context = _rid_type.context
                else:
                    context = _rid_type         
            
                self._action_table[(action_type, context)] = func
            
            return func
        return decorator
    
    def execute(self, action_type: str, rid: RID, *args, **kwargs):
        action_pair = (action_type, rid.context)
        if action_pair in self._action_table:
            func = self._action_table[action_pair]
            return func(rid, *args, **kwargs)
        else:
            return None
        
    def register_dereference(self, *args, **kwargs):
        return self.register(ActionType.dereference, *args, **kwargs)
        
    def dereference(
        self, 
        rid: RID, 
        hit_cache=True, # tries to read cache first, writes to cache if there is a miss
        refresh=False   # refreshes cache even if there was a hit
    ):
        if self.cache is not None and hit_cache is True and refresh is False:
            bundle = self.cache.read(rid)
            if bundle is not None:
                print("hit cache")
                return bundle
        
        raw_data = self.execute(ActionType.dereference, rid)        
        manifest = Manifest.generate(rid, raw_data)
        bundle = CacheBundle(manifest, raw_data)
        
        if self.cache is not None and hit_cache is True:
            self.cache.write(rid, bundle)
        
        return bundle
