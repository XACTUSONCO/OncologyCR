! function() {
    "use strict";

    function i(t) {
        document.getElementById(t) && (document.getElementById(t).checked = !0)
    }
	
    function s() {
        setTimeout(function() {
            var e, t, a = document.getElementById("accordion");
            a && (a = a.querySelector(".mm-active .active"), 300 < (e = a ? a.offsetTop : 0) && (e -= 100, (t = document.getElementsByClassName("vertical-menu") ? document.getElementsByClassName("vertical-menu")[0] : "") && t.querySelector(".simplebar-content-wrapper") && setTimeout(function() {
                t.querySelector(".simplebar-content-wrapper").scrollTop = e
            }, 0)))
        }, 0)
    }

    var t, e;
    //feather.replace(), 
		window.sessionStorage && ((t = sessionStorage.getItem("is_visited")) ? document.querySelector("#" + t) : sessionStorage.setItem("is_visited", "layout-direction-ltr")),
        function() {
            var e = document.body.getAttribute("data-sidebar-size");
            window.onload = function() {
                1024 <= window.innerWidth && window.innerWidth <= 1366 && (document.body.setAttribute("data-sidebar-size", "sm"), i("sidebar-size-small"))
            };
            for (var t = document.getElementsByClassName("vertical-menu-btn"), a = 0; a < t.length; a++) t[a] && t[a].addEventListener("click", function(t) {
                t.preventDefault(), document.body.classList.toggle("sidebar-enable"), 
				362 <= window.innerWidth ? null == e ? null == document.body.getAttribute("data-sidebar-size") || "lg" == document.body.getAttribute("data-sidebar-size") ? document.body.setAttribute("data-sidebar-size", "sm") : document.body.setAttribute("data-sidebar-size", "lg") : "md" == e ? "md" == document.body.getAttribute("data-sidebar-size") ? document.body.setAttribute("data-sidebar-size", "sm") : document.body.setAttribute("data-sidebar-size", "md") : "sm" == document.body.getAttribute("data-sidebar-size") ? document.body.setAttribute("data-sidebar-size", "lg") : document.body.setAttribute("data-sidebar-size", "sm") : s()
            })
        }(), setTimeout(function() {
            var t = document.querySelectorAll("#sidebar-menu a");
            t && t.forEach(function(t) {
                var e, a, i, n, o, s = window.location.href;
                t.href == s && (t.classList.add("active"), (e = t.parentElement) && "accordion" !== e.id && (e.classList.add("mm-active"), (a = e.parentElement) && "accordion" !== a.id && (a.classList.add("mm-show"), a.classList.contains("mm-collapsing") && console.log("has mm-collapsing"), (i = a.parentElement) && "accordion" !== i.id && (i.classList.add("mm-active"), (n = i.parentElement) && "accordion" !== n.id && (n.classList.add("mm-show"), (o = n.parentElement) && "accordion" !== o.id && o.classList.add("mm-active"))))))
            })
        }, 0), setTimeout(function() {
            var t = document.querySelectorAll("#submenu-tab a");
            t && t.forEach(function(t) {
                var e, a, i, n, o, s = window.location.href.split(/[?#]/)[0];
                t.href == s && (t.classList.add("active"), (e = t.parentElement) && "accordion" !== e.id && (e.classList.add("mm-active"), (a = e.parentElement) && "accordion" !== a.id && (a.classList.add("mm-show"), a.classList.contains("mm-collapsing") && console.log("has mm-collapsing"), (i = a.parentElement) && "accordion" !== i.id && (i.classList.add("mm-active"), (n = i.parentElement) && "accordion" !== n.id && (n.classList.add("mm-show"), (o = n.parentElement) && "accordion" !== o.id && o.classList.add("mm-active"))))))
            })
        }, 0),
			[].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]')).map(function(t) {
            return new bootstrap.Tooltip(t)
        }), [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]')).map(function(t) {
            return new bootstrap.Popover(t)
        }), [].slice.call(document.querySelectorAll(".toast")).map(function(t) {
            return new bootstrap.Toast(t)
        })
//sessionStorage.clear();
}();


// toggle full screen
function toggleFullScreen() {
    if (!document.fullscreenElement && // alternative standard method
        !document.mozFullScreenElement && !document.webkitFullscreenElement) { // current working methods
        if (document.documentElement.requestFullscreen) {
            document.documentElement.requestFullscreen();
        } else if (document.documentElement.mozRequestFullScreen) {
            document.documentElement.mozRequestFullScreen();
        } else if (document.documentElement.webkitRequestFullscreen) {
            document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
        }
    } else {
        if (document.cancelFullScreen) {
            document.cancelFullScreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
            document.webkitCancelFullScreen();
        }
    }
}



$(document).ready(function(){	

	if($("#accordion li").hasClass("mm-show") === true) {

		// 속성값이 존재함.
		//alert("ok");
		$("#accordion li.mm-show").children("a").attr("aria-expanded", "true");
		$("#accordion li.mm-show").children("a").removeClass("collapsed");
		$("#accordion li.mm-show").children("div").addClass("show");
		

	}
        // 3차 뎁스 추가
	if($("#accordion > li > div > ul").hasClass("mm-show") === true) {
		// 속성값이 존재함.
		//alert("ok");
		$("#accordion > li > div.mm-active").addClass("show");
		$("#accordion > li > div.mm-active").parent('li').addClass("mm-show");
	}

	$('.agree-scroll').overlayScrollbars({
		className: "os-theme-dark",
		resize: "none",
		sizeAutoCapable: true,
		paddingAbsolute: true
	});
	
	//약관 동의
	$('input[type="checkbox"][id="agree-check1"]').on('click', function(){
		var chkValue = $('input[type="checkbox"][id="agree-check1"]:checked').val();
		if(chkValue){
			 $(".agree-step-btn1").show();
		}else{
			 $(".agree-step-btn1").hide();
		}
	}); 
	$('input[type="checkbox"][id="agree-check2"]').on('click', function(){
		var chkValue = $('input[type="checkbox"][id="agree-check2"]:checked').val();
		if(chkValue){
			 $(".agree-step-btn2").show();
		}else{
			 $(".agree-step-btn2").hide();
		}
	}); 

	//회원가입 다음
	$(".agree-step-btn1").click(function () {
		$(".signup-area .nav-tabs .step1 .nav-link").removeClass("active");
		$(".signup-area .nav-tabs .step2 .nav-link").addClass("active");
		$("#menu1").removeClass("active");
		$("#menu2").addClass("active");
		$("#menu2").addClass("show");
	}); 
	$(".agree-step-btn2").click(function () {
		$(".signup-area .nav-tabs .step2 .nav-link").removeClass("active");
		$(".signup-area .nav-tabs .step3 .nav-link").addClass("active");
		$("#menu2").removeClass("active");
		$("#menu3").addClass("active");
		$("#menu3").addClass("show");
	}); 


	/* 프린트 */
	$("#print").click(function () {
		let $container = $("#printArea").clone()
		/** 팝업 */
		let innerHtml = $container[0].innerHTML
		let popupWindow = window.open("", "_blank", "width=700,height=800")
		popupWindow.document.write( "<head>");
		popupWindow.document.write("<link rel='stylesheet' type='text/css' href='./assets/css/bootstrap.min.css'>");
		popupWindow.document.write("<link rel='stylesheet' type='text/css' href='./assets/css/bootstrap-icons.css'>");
		popupWindow.document.write("<link rel='stylesheet' type='text/css' href='./assets/css/icons.min.css'>");
		popupWindow.document.write("<link rel='stylesheet' type='text/css' href='./assets/css/plugins.css'>");
		popupWindow.document.write("<link rel='stylesheet' type='text/css' href='./assets/css/style.css'>");
		popupWindow.document.write("<link rel='stylesheet' type='text/css' href='./assets/css/print.css'>");
		popupWindow.document.write("<script src='./assets/libs/jquery/jquery.min.js'></script>");
		popupWindow.document.write("<script src='./assets/libs/bootstrap/js/bootstrap.bundle.min.js'></script>");
		popupWindow.document.write("<script src='./assets/libs/simplebar/simplebar.min.js'></script>");
		popupWindow.document.write("<script src='./assets/js/plugins.js'></script>");
		popupWindow.document.write("<script src='./assets/js/active.js'></script>");
		popupWindow.document.write( '</head>' );
		popupWindow.document.write( '<body>' );
		popupWindow.document.write( '<div>' );
		popupWindow.document.write( innerHtml );
		popupWindow.document.write( '</div></body>' );
	   
		popupWindow.document.close()
		popupWindow.focus()

		/** 1초 지연 */
		setTimeout(function(){
			popupWindow.print()         
			popupWindow.close()     
		}, 1000)
	})
});


$(function () {
        let trs = $('table tr.table-link');

        for (let i = 0; i < trs.length; i++) {
            const tr = trs[i];
            const link = tr.getAttribute('data-link');

            const tds = $(tr).find('td');
            for (let j = 0; j < tds.length; j++) {
                const td = tds[j];
                if (!td.hasAttribute('data-link-disabled')) {
                    $(td).click(function (e) {
                        e.preventDefault();
                        window.location = link;
                    });
                }
            }
        }
    }
);



