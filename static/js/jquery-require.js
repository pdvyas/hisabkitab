(function($) {
    $.require = function(files, params) {
        var params = params || {}; 

        if (!$.require.loaded)
            $.require.loaded = {};

        if (!$.require.path )
            $.require.path = '';

        if (typeof files === "string") {
            files = new Array(files);
        }
        $.each(files, function(n, file) {
            if (!$.require.loaded[file]) {
                var extn = file.split('.').slice(-1);
                xhr = $.ajax({
                    type: "GET",
                    url: $.require.path + files[n],
                    success: params.callback || null,
                    datatype: extn=="js" ? "script" : "text",
                    cache: params.cache===false?false:true,
                    async: false
                });
                $.require.loaded[file] = true;
                if(extn=="css") {
                    $.set_style(xhr.responseText);
                }
            }
        })
        //console.dir($.require.loaded);

        return $;
    };
})(jQuery);
