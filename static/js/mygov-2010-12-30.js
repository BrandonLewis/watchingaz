mg = YUI.namespace("mg");
YUI().add("mygov", function(Y) {

    var Lang = Y.Lang,
        Node = Y.Node;
    var MyGov,
        Options,
        MYGOV = 'myGov',
        CACHE_SANDBOX = 'mg';
        
    Options = function(config){
        Options.superclass.constructor.apply(this, arguments);
    }
    
    Y.mix(Options, {
        NAME : 'options',
        ATTRS : {
            beta: {
                value: false,
                validator: Lang.isBoolean
            },
            color: {
                value: '',
                validator: Lang.isString
            }
        }
    });
    
    Y.extend(Options, Y.Base);
    
    MyGov = function(config){
        MyGov.superclass.constructor.apply(this, arguments);
    }
    /* static */
    Y.mix(MyGov, {
        NAME : MYGOV,
        ATTRS : {
            status: {
                value: '',
                validator: Lang.isString
            },
            sandbox: {
                value: CACHE_SANDBOX
            },
            options: {
                value: null
            },
            restore: {
                value: false
            }
        }
    });
    /* prototype */
    Y.extend(MyGov, Y.Base, {
        _cache : null,
        _history : null,
        _queue : null,
        _datasources : [],
        _schemas : {
            base_bill: {
                        metaFields: {
                            totalPages:"ResultSet.total",
                            nextPage:"ResultSet.next",
                            prevPage:"ResultSet.previous",
                            curPage:"ResultSet.current"
                            },
                        resultListLocator: "ResultSet.Result",
                        resultFields: ["url","bill_number","title"]
                    }
        },
        
        initializer : function(config){
            this._cache = new Y.CacheOffline({sandbox:CACHE_SANDBOX});
            this._history = new Y.History();
            this._queue = new Y.AsyncQueue();
            if (config && config.options){
                this.options = new Options(config.options);
            } else {
                this.options = new Options();
            }
        },
        
        destructor : function() {
            this._queue = null;
        },
        
        _restoreItem : function(key) {
            var item = this._cache.retrieve(key);
            return item ? item.response : false;
        },
        
        _saveItem : function(key, value) {
            if (value instanceof Y.DataSource){
                
            }
            this._cache.add(key, value);
        },
        /* Public */
        
        /* saves and item to the cache */
        saveItem : function(key, value) {
            this._saveItem(key, value);
        },
        
        restoreItem : function(key) {
            return this._restoreItem(key);
        },
        
        getDataSource : function() {
            
        }
    });
    Y.MyGov = MyGov;
}, '@VERSION@' , {requires:["base-base", "cookie", "history", "cache-offline", "async-queue", "io"]});
