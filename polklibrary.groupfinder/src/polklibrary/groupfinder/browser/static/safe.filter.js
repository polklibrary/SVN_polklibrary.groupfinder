

var SafeFilter = {

    BANNED_PHRASES : [' ass ',' fuck','fuck ','bitch',' shit','shit ','asshole','cocksucker',' cock','http'],

    init : function() {
        $('.pat-safefilter').keydown(function(){
            var text = $(this).text();
            if (typeof text === 'undefined' || text == null || text == '')    
                text = $(this).val();
                
            for (var i in SafeFilter.BANNED_PHRASES){
            
                if (text.toLowerCase().indexOf(SafeFilter.BANNED_PHRASES[i]) != -1) {
                    $(this).val(text.replace(SafeFilter.BANNED_PHRASES[i],''));
                    $(this).text(text.replace(SafeFilter.BANNED_PHRASES[i],''));
                    alert('Removed inappropriate word or phrase.');
                }
            }
        });
    },
    
    
}

$(document).ready(function(){
    SafeFilter.init();
});