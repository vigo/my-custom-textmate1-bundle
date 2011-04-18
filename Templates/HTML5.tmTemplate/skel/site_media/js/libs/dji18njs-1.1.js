// *********************************************************
// dji18njs
// 
// *********************************************************
(function(){
    window.dji18njs = {
        version: "1.1",
        catalog: { en: new Array() },
        lang_id: 'en',
        get_msg: function(msgid){
            if(typeof(this.catalog[this.lang_id][msgid]) == 'undefined'){
                return msgid;
            } else {
                return this.catalog[this.lang_id][msgid];
            }
        },
        gettext: function(msgid){
            var value = this.get_msg(msgid);
            if(typeof(value) == 'undefined'){
                return msgid;
            } else {
                return (typeof(value) == 'string') ? value : value[0];
            }
        },
        ngettext: function(singular, plural, count){
            var value_singular = this.get_msg(singular),
                value_plural = this.get_msg(plural);
            if(count == 0){
                return value_singular;
            }
            return (count == 1) ? value_singular : value_plural;
        },
        interpolate: function(fmt, obj, named){
            fmt = this.get_msg(fmt);
            if(named){
                return fmt.replace(/%\(\w+\)s/g, function(match){
                    var replace_val = String(obj[match.slice(2,-2)]);
                    if( replace_val == 'undefined'){
                        return "?" + match + "?";
                    }
                    return replace_val;
                });
            } else {
                return fmt.replace(/%s/g, function(match){
                    return String(obj.shift())
                });
            }
        }
    }
})();

