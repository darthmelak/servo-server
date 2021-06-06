jQuery(function($) {
    var img = {
        $el: $('img'),
        isLive: false,
        url: {
            ph: $('img').attr('src'),
            live: $('img').data('livesrc'),
        },
    }

    var isTouchDevice = "ontouchstart" in document.documentElement ? true : false
    var BUTTON_DOWN   = isTouchDevice ? "touchstart" : "mousedown"
    var BUTTON_UP     = isTouchDevice ? "touchend"   : "mouseup"
    
    $("button.dir").bind(BUTTON_DOWN, function() {
        fetch("/cmd", {
            method: "POST",
            body: this.id,
        })
    })

    $("button.dir").bind(BUTTON_UP, function() {
        fetch("/cmd", {
            method: "POST",
            body: "stop",
        })
    })

    $("button#start").on("click", function () {
        img.isLive = !img.isLive
        img.$el.attr('src', img.isLive ? img.url.live : img.url.ph)
    })

    $("input").change(function() {
        var speed = this.value
        fetch("/cmd", {
            method: "POST",
            body: JSON.stringify({ speed: speed }),
        })
    })
})
