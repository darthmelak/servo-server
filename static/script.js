(function (d) {
    $img = d.querySelector("img")
    var img = {
        $el: $img,
        isLive: false,
        url: {
            ph: $img.getAttribute("src"),
            live: $img.dataset.livesrc.replace(/\$host\$/, window.location.hostname),
        },
    }
    var $STRTbtn = d.querySelector("button#start")
    var $NVbtn = d.querySelector("button#nv")
    var $LEDbtn = d.querySelector("button#led")
    var $DIRbtns = d.querySelectorAll("button.dir")

    var nv = $NVbtn.classList.contains('active')
    var led = $LEDbtn.classList.contains('active')

    var isTouchDevice = "ontouchstart" in d.documentElement ? true : false
    var BUTTON_DOWN   = isTouchDevice ? "touchstart" : "mousedown"
    var BUTTON_UP     = isTouchDevice ? "touchend"   : "mouseup"

    for (let $btn of $DIRbtns) {
        $btn.addEventListener(BUTTON_DOWN, function (ev) {
            fetch("/cmd", {
                method: "POST",
                body: ev.target.id,
            })
        })

        $btn.addEventListener(BUTTON_UP, function (ev) {
            fetch("/cmd", {
                method: "POST",
                body: "stop",
            })
        })
    }

    $STRTbtn.addEventListener("click", function (ev) {
        img.isLive = !img.isLive
        img.$el.setAttribute("src", img.isLive ? img.url.live : img.url.ph)
        ev.target.classList[img.isLive ? "add" : "remove"]("active")
    })

    $NVbtn.addEventListener("click", function (ev) {
        nv = !nv
        fetch("/cmd", {
            method: "POST",
            body: nv ? "nvstart" : "nvstop",
        })
        ev.target.classList[nv ? "add" : "remove"]("active")
    })

    $LEDbtn.addEventListener("click", function (ev) {
        led = !led
        fetch("/cmd", {
            method: "POST",
            body: "ledswitch",
        })
        ev.target.classList[led ? "add" : "remove"]("active")
    })
})(document)
