(function (d) {
    $img = d.querySelector("img")
    const img = {
        $el: $img,
        isLive: false,
        url: {
            ph: $img.getAttribute("src"),
            live: $img.dataset.livesrc.replace(/\$host\$/, window.location.hostname),
        },
    }

    const STEP = 30

    let offsetTop = 0
    let offsetLeft = 0
    let startX = 0
    let startY = 0
    let started = false
    let prevStepX = 0
    let prevStepY = 0

    const $STRTbtn = d.querySelector("button#start")
    const $NVbtn = d.querySelector("button#nv")
    const $LEDbtn = d.querySelector("button#led")
    const $DIRbtns = d.querySelectorAll("button.dir")
    const $Gyrobtn = d.querySelector("button#gyro")
    const $TouchO = d.querySelector(".touch-overlay")
    const $TouchM = d.querySelector(".touch-marker")
    const $canvas = d.querySelector(".touch-overlay canvas")
    const ctx = $canvas.getContext("2d")

    let nv = $NVbtn.classList.contains("active")
    let led = $LEDbtn.classList.contains("active")

    const isTouchDevice = "ontouchstart" in d.documentElement ? true : false
    const BUTTON_DOWN   = isTouchDevice ? "touchstart" : "mousedown"
    const BUTTON_UP     = isTouchDevice ? "touchend"   : "mouseup"
    const MOVE          = isTouchDevice ? "touchmove"  : "mousemove"

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

    window.addEventListener('resize', resizectx, false)
    function resizectx() {
        $canvas.width = $TouchO.offsetWidth
        $canvas.height = $TouchO.offsetHeight
        offsetLeft = $TouchO.offsetLeft
        offsetTop = $TouchO.offsetTop
    }
    resizectx()

    function moveMarker({x, y}) {
        $TouchM.style.left = `${x}px`
        $TouchM.style.top = `${y}px`
    }

    function getCoords(event) {
        let ev = event
        if (event instanceof TouchEvent) {
            ev = event.touches[0]
        }

        return {
            x: ev.clientX - offsetLeft,
            y: ev.clientY - offsetTop,
        }
    }

    $TouchO.addEventListener(BUTTON_DOWN, function (ev) {
        const c = getCoords(ev)
        startX = c.x
        startY = c.y
        moveMarker(c)
        started = true
        $TouchM.classList.add("active")
    })

    $TouchO.addEventListener(BUTTON_UP, function (ev) {
        started = false
        ctx.reset()
        $TouchM.classList.remove("active")
        fetch("/cmd", {
            method: "POST",
            body: "stop",
        })
    })

    const onMove = function (ev) {
        ev.preventDefault()
        if (started) {
            const c = getCoords(ev)
            ctx.reset()
            ctx.strokeStyle = "#FFFF00"
            ctx.beginPath()
            ctx.moveTo(startX, startY)
            ctx.lineTo(c.x, c.y)
            ctx.stroke()
            ctx.closePath()

            const stepX = Math.round((c.x - startX) / STEP)
            const stepY = Math.round((c.y - startY) / STEP)

            if (stepX !== prevStepX || stepY !== prevStepY) {
                fetch("/speed", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({stepX, stepY}),
                })
            }

            if (stepX !== prevStepX) { prevStepX = stepX }
            if (stepY !== prevStepY) { prevStepY = stepY }
        }
    }

    $TouchO.addEventListener(MOVE, _.throttle(onMove, 250, {leading: true, trailing: true}))
})(document)
