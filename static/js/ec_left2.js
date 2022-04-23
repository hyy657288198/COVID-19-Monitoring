function start_roll() {
    const speed = 30; // Speed of text scrolling
    const wrapper = document.getElementById('risk_wrapper');
    const li1 = document.getElementById('risk_wrapper_li1');
    const li2 = document.getElementById('risk_wrapper_li2');
    li2.innerHTML = li1.innerHTML; //Clone content
    function Marquee() {
        if (li2.offsetHeight - wrapper.scrollTop <= 0) //When scrolling to the junction of demo1 and demo2
            wrapper.scrollTop -= li1.offsetHeight; //demo jumps to the top
        else {
            wrapper.scrollTop++
        }
    }

    let MyMar = setInterval(Marquee, speed); //set timer
    wrapper.onmouseover = function () {
        clearInterval(MyMar)    //Clear the timer when the mouse moves up to achieve the purpose of rolling stop
    };
    wrapper.onmouseout = function () {
        MyMar = setInterval(Marquee, speed)  //Reset timer when mouse is removed
    }
}
