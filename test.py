import beaker.cache, beaker.util


cache_opts = {
    'cache.type':       'file',
    'cache.data_dir':   'var/cache',
    'cache.lock_dir':   'var/cachelck',
    'expire':           3600
}
cm = beaker.cache.CacheManager(**beaker.util.parse_cache_config_options(cache_opts))


def return_stuff():
    print( "here" )
    return "blarg"

cache = cm.get_cache("flurble")
print( cache )
quit()
key = "blargle"
rv = cache.get( key = key, createfunc = return_stuff )
print( rv )

