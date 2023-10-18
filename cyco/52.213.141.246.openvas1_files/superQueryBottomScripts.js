var showLandingPage = false;

function loadBundle(version) {
    var animationInterval;
    document.getElementById("index_progress_border").style.width = '10%';

    function updateProgress(xhr) {
        var p = Math.round((xhr.loaded / xhr.total) * 100);
        //dont load 100% of the progress if we need to load the data
        //              if (localStorage.STORAGE_GC_STATUSV6 && JSON.parse(localStorage.STORAGE_GC_STATUSV6).projects && JSON.parse(localStorage.STORAGE_GC_STATUSV6).projects.length == 0) {
        //                p = p / 2
        //              }
        if (location.href.toString().indexOf('#code') > -1) {
            p = p / 2;
        }
        if (p > 10) {
            document.getElementById("index_progress_border").style.width = p + '%';
        }
    }

    function getEnv() {
        var hostname = window.location.hostname;
        var url;
        switch (hostname) {
            case 'localhost':
                url = 'https://localhost:8080';
                break;
            case 'dev.evaluex.io':
                url = `https://devapi4.evaluex.io/stage4`;
                break;
            default:
                url = 'https://api4.superquery.io/stage4';
                break;
        }
        return url;
    }

    function delayRequest(time) {
        var url = getEnv();
        var reqUrl = `${url}/goog/delayRequest`;
        var http = new XMLHttpRequest();
        var mydata = {
            time
        };
        http.open('POST', reqUrl, true);
        http.setRequestHeader("Content-Type", "application/json");
        http.send(JSON.stringify(mydata));
    }

    function readBody(xhr) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/bundle.js?version=' + version);
        xhr.addEventListener("progress", updateProgress, false);
        xhr.onload = function () {
            if (xhr.status === 200) {
                eval(xhr.responseText);
                if (localStorage.STORAGE_GC_STATUSV6 && JSON.parse(localStorage.STORAGE_GC_STATUSV6).projects && JSON
                    .parse(localStorage.STORAGE_GC_STATUSV6).projects.length == 0) {
                } else if (location.href.toString()
                    .indexOf('#code') > -1) {
                } else {
                    document.getElementById("index_progress_border").style.width = '100%';
                }
                setTimeout(async () => {
                    if (!showLandingPage) {
                        //                      eval(xhr.responseText)
                        if (location.href.toString().indexOf('#code') == -1) {
                            //Case linked account flow show linkAccount modal
                            //dont hide the loading splash screen until we call the api of getGoogleJobList in app.js
                            //the hide of the splash screen is in app.js
                            document.getElementById("index_progress").style.display = 'none';
                            if (document.getElementsByClassName("index_animation_container") && document.getElementsByClassName(
                                "index_animation_container")[0]) {
                                document.getElementsByClassName("index_animation_container")[0].style.display = 'none';
                            }
                        }
                        clearInterval(animationInterval);
                    }
                }, 300);

            } else {
                console.error('error when try to load bundle.js');
            }
        };
        xhr.send();
    }

    setTimeout(() => {

        //readBody();
    }, 1);
}


//'use strict';
/*mor code*/
// var animation = {
//   chars: ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
//     'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
//   ],
//   init: function () {
//     if (showLandingPage) {
//       return
//     }
//     animation.container = document.createElement('div');
//
//     animation.container.className = 'index_animation_container';
//     if (document.getElementById('index_progress')) {
//       document.getElementById('index_progress').appendChild(animation.container);
//     }
//     animationInterval = setInterval(animation.add, 150);
//   },
//   add: function () {
//     if (document.getElementsByClassName('index_animation_container')[0].style.display != 'none') {
//       var element = document.createElement('span');
//       animation.container.appendChild(element);
//       animation.animate(element);
//     }
//   },
//   animate: function (element) {
//     if(!element){
//       return
//     }
//     var character = animation.chars[Math.floor(Math.random() * animation.chars.length)];
//     var duration = Math.floor(Math.random() * 15) + 1;
//     var offset = Math.floor(Math.random() * (50 - duration * 2)) + 3;
//     var size = 10 + (15 - duration);
//     element.style.cssText = 'right:' + offset + 'vw; font-size:' + size + 'px;animation-duration:' +
//       duration + 's';
//     element.innerHTML = character;
//     window.setTimeout(animation.remove, duration * 1000, element);
//   },
//   remove: function (element) {
//     if(!element){
//       return
//     }
//     element.parentNode.removeChild(element);
//   },
// };
//document.addEventListener('DOMContentLoaded', animation.init);


function installAnalytics() {
    // Google Analytics
    // (function (i, s, o, g, r, a, m) {
    //     i['GoogleAnalyticsObject'] = r;
    //     i[r] = i[r] || function () {
    //         (i[r].q = i[r].q || []).push(arguments);
    //     }, i[r].l = 1 * new Date();
    //     a = s.createElement(o),
    //         m = s.getElementsByTagName(o)[0];
    //     a.async = 1;
    //     a.src = g;
    //     m.parentNode.insertBefore(a, m);
    // })(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');
    // ga('create', 'UA-101099797-1', 'auto');
    // ga('send', 'pageview');
}

function installIntercom() {
    window.intercomSettings = {
        app_id: "a6n7brm4"
    };
    (function () {
        var w = window;
        var ic = w.Intercom;
        if (typeof ic === "function") {
            ic('reattach_activator');
            ic('update', intercomSettings);
        } else {
            var d = document;
            var i = function () {
                i.c(arguments);
            };
            i.q = [];
            i.c = function (args) {
                i.q.push(args);
            };
            w.Intercom = i;
            window.index_loadIntercom = function l() {
                if (!w.Intercom) {
                    return;
                }
                var s = d.createElement('script');
                s.type = 'text/javascript';
                s.async = true;
                s.src = 'https://widget.intercom.io/widget/a6n7brm4';
                var x = d.getElementsByTagName('script')[0];
                x.parentNode.insertBefore(s, x);
                w.Intercom('onHide', function () {
                    //            setTimeout(() => {
                    //              $("#intercom-container").fadeOut()
                    //            }, 500)
                });
                w.Intercom('onUnreadCountChange', function () {
                    $("#intercom-container").fadeIn();
                });
            };
        }
    })();
}

function installHotJar() {
    let locationLink = location.href.toString();
    if (locationLink.indexOf('evaluex') > -1) { //for evaluex
        (function (h, o, t, j, a, r) {
            h.hj = h.hj || function () {
                (h.hj.q = h.hj.q || []).push(arguments);
            };
            h._hjSettings = {
                hjid: 864118,
                hjsv: 6
            };
            a = o.getElementsByTagName('head')[0];
            r = o.createElement('script');
            r.async = 1;
            r.src = t + h._hjSettings.hjid + j + h._hjSettings.hjsv;
            a.appendChild(r);
        })(window, document, 'https://static.hotjar.com/c/hotjar-', '.js?sv=');
    } else { //for superquery
        (function (h, o, t, j, a, r) {
            h.hj = h.hj || function () {
                (h.hj.q = h.hj.q || []).push(arguments);
            };
            h._hjSettings = {
                hjid: 864112,
                hjsv: 6
            };
            a = o.getElementsByTagName('head')[0];
            r = o.createElement('script');
            r.async = 1;
            r.src = t + h._hjSettings.hjid + j + h._hjSettings.hjsv;
            a.appendChild(r);
        })(window, document, 'https://static.hotjar.com/c/hotjar-', '.js?sv=');
    }
}

function installWebworker() {
    var channel = new MessageChannel();
    console.log('CLIENT: service worker registration in progress.');
    //      navigator.serviceWorker.register( URL.createObjectURL(blob)).then((w)=> {
    var webWorkerPath = 'demo_workers.js';
    navigator.serviceWorker.register(`${webWorkerPath}?v=${(new Date()).getTime()}`).then((worker1) => {
        console.log('CLIENT: service worker registration complete.');
        channel.port2.onmessage = (messageEvent) => {
            if (messageEvent.data.newVersion) {
                var session = localStorage.session;
                localStorage.clear();
                if (session) {
                    localStorage.session = session;
                }
            }
            window.exVersion = messageEvent.data.version;
            // loadBundle(messageEvent.data.version)
            console.log("CLIENT: version:", messageEvent.data.version);
        };
        setTimeout(() => {
            worker1.active.postMessage({
                command: "connect"
            }, [channel.port1]);
        }, 2000);
    }, function () {
        console.log('CLIENT: service worker registration failure.');
    });
}

function getQueryParams(queryString) {
    if(!queryString){return {}}

    const paramsObj = {};
    const paramsArr = queryString.split('&');
    paramsArr.forEach(param => {
        const paramArr = param.split('=');
        if (paramArr && paramArr[0] && paramArr[1]) {
            paramsObj[paramArr[0]] = paramArr[1];
        }
    });
    return paramsObj;
}


function linkAccount(longUrl, type, data) {
    return new Promise(resolved => {
        $.ajax({
            url: longUrl,
            type,
            data: (type == 'post') ? JSON.stringify(data) : data,
            contentType: "application/x-www-form-urlencoded",
            dataType: "json",
            success: (res) => {
                openModal('paymentMade');
                localStorage.removeItem("gcp");
                resolved(true);
            },
            error: (err) => {
                console.log(err);
                localStorage.removeItem("gcp");
                resolved(false);
            }
        });
    });
}

async function linkAccountFlow(gcp) {
    openModal('paymentMade');
    console.log("linkAccountFlow starting");
    const session = localStorage.getItem('session');
    console.log(`linkAccountFlow session:${session} gcp:${gcp}`);
    return (session && gcp) ? linkAccount('https://gcp.superquery.io/stagegcp/goog/gcpmarket', 'post', {
        session,
        gcp
    }) : false;
}


// installIntercom();
let locationLink = location.href.toString();
if (locationLink.indexOf('https://dev.evaluex.io/') == -1 && locationLink.indexOf('https://localhost') == -1 && locationLink.indexOf('https://localhost') == -1) {
    if (localStorage.session) {
        // if (localStorage.session && localStorage.machineId) {} else {}
        // installHotJar();
        installAnalytics();
    }
    if (navigator.userAgent.indexOf('Chrome') > -1) {
        installWebworker();
    } else { //if its not chrome the webworker will not work
        // loadBundle('')
    }
} else { // if the user is in p.evaluex.io
    //    installWebworker();
    // loadBundle('')
}

function openModal(modalType) {
    hideAllModals();
    if (document.getElementById('index_progress')) {
        document.getElementById('index_progress').style.display = 'none';
    }
    switch (modalType) {
        case 'login':
            $("#app").hide();
            $("#index_body").show();
            if (document.getElementById('index_extentionPage')) {
                document.getElementById('index_extentionPage').style.display = 'block';
            }
            break;
        case 'paymentMade':
            $("#app").hide();
            $("#index_body").show();
            if (document.getElementById('index_payment-made')) {
                document.getElementById('index_payment-made').style.display = 'block';
            }
            break;
        case 'localstorageMessage':
            $("#app").hide();
            $("#index_body").show();
            if (document.getElementById('index_localstorage')) {
                document.getElementById('index_localstorage').style.display = 'block';
            }
            break;
    }
}

function hideAllModals() {
    document.getElementById('index_extentionPage').style.display = 'none';
    document.getElementById('index_payment-made').style.display = 'none';
    document.getElementById('index_localstorage').style.display = 'none';
}


// Active campaign pixel
var trackByDefault = true;

function acEnableTracking() {
    var expiration = new Date(new Date().getTime() + 1000 * 60 * 60 * 24 * 30);
    document.cookie = "ac_enable_tracking=1; expires= " + expiration + "; path=/";
    acTrackVisit();
}

function acTrackVisit() {
    var trackcmp_email = '';
    var trackcmp = document.createElement("script");
    trackcmp.async = true;
    trackcmp.type = 'text/javascript';
    trackcmp.src = '//trackcmp.net/visit?actid=1000048128&e=' + encodeURIComponent(trackcmp_email) + '&r=' +
        encodeURIComponent(document.referrer) + '&u=' + encodeURIComponent(window.location.href);
    var trackcmp_s = document.getElementsByTagName("script");
    if (trackcmp_s.length) {
        trackcmp_s[0].parentNode.appendChild(trackcmp);
    } else {
        var trackcmp_h = document.getElementsByTagName("head");
        trackcmp_h.length && trackcmp_h[0].appendChild(trackcmp);
    }
}

if (trackByDefault || /(^|; )ac_enable_tracking=([^;]+)/.test(document.cookie)) {
    acEnableTracking();
}


!function (f, b, e, v, n, t, s) {
    if (f.fbq) return;
    n = f.fbq = function () {
        n.callMethod ?
            n.callMethod.apply(n, arguments) : n.queue.push(arguments);
    };
    if (!f._fbq) f._fbq = n;
    n.push = n;
    n.loaded = !0;
    n.version = '2.0';
    n.queue = [];
    t = b.createElement(e);
    t.async = !0;
    t.src = v;
    s = b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t, s);
}(window, document, 'script',
    'https://connect.facebook.net/en_US/fbevents.js');

fbq('init', '416296055481040');
fbq('track', 'PageView');


//
//
// (function (e, a) {
//   if (!a.__SV) {
//     var b = window;
//     try {
//       var c, l, i, j = b.location,
//         g = j.hash;
//       c = function (a, b) {
//         return (l = a.match(RegExp(b + "=([^&]*)"))) ? l[1] : null
//       };
//       g && c(g, "state") && (i = JSON.parse(decodeURIComponent(c(g, "state"))), "mpeditor" === i.action && (b.sessionStorage
//           .setItem("_mpcehash", g), history.replaceState(i.desiredHash || "", e.title, j.pathname + j.search)
//       ))
//     } catch (m) {}
//     var k, h;
//     window.mixpanel = a;
//     a._i = [];
//     a.init = function (b, c, f) {
//       function e(b, a) {
//         var c = a.split(".");
//         2 == c.length && (b = b[c[0]], a = c[1]);
//         b[a] = function () {
//           b.push([a].concat(Array.prototype.slice.call(arguments,
//             0)))
//         }
//       }
//
//       var d = a;
//       "undefined" !== typeof f ? d = a[f] = [] : f = "mixpanel";
//       d.people = d.people || [];
//       d.toString = function (b) {
//         var a = "mixpanel";
//         "mixpanel" !== f && (a += "." + f);
//         b || (a += " (stub)");
//         return a
//       };
//       d.people.toString = function () {
//         return d.toString(1) + ".people (stub)"
//       };
//       k =
//         "disable time_event track track_pageview track_links track_forms register register_once alias unregister identify name_tag set_config reset people.set people.set_once people.increment people.append people.union people.track_charge people.clear_charges people.delete_user"
//           .split(" ");
//       for (h = 0; h < k.length; h++) e(d, k[h]);
//       a._i.push([b, c, f])
//     };
//     a.__SV = 1.2;
//     b = e.createElement("script");
//     b.type = "text/javascript";
//     b.async = !0;
//     b.src = "undefined" !== typeof MIXPANEL_CUSTOM_LIB_URL ? MIXPANEL_CUSTOM_LIB_URL : "file:" === e.location.protocol &&
//     "//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js".match(/^\/\//) ?
//       "https://cdn.mxpnl.com/libs/mixpanel-2-latest.min.js" : "//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js";
//     c = e.getElementsByTagName("script")[0];
//     c.parentNode.insertBefore(b, c)
//   }
// })(document, window.mixpanel || []);
// mixpanel.init("32eb19b40c05afdf85fa40c0e1368d9c");
//
// console.log('hi bottom')


indexClass();
var startNumber = 67152127;

function indexClass() {
    constructor();

    function constructor() {
        $('#landingPage_loginButton_button1, #landingPage_loginButton_button2').click(login);
        $('.landingPage_loginButton_input').keyup(checkIfClickEnter);
        $(".index_extentionPage_box_button").click(loginFromExtention);
        $(".index_payment-made_box_button").click(closePaymentModal);
        $(".index_localstorage_box_button").click(openInNewPage);
        $(".LandingPageLogin_googleLogin").click(gotToLogin);
        $(".LandingPageLogin_close").click(hideLogin);
        $(".landingPage_login").click(loginFromExtention);
        $(".LandingPageContact_left_box_row_button").click(contactUs);
        $(".LandingPageLogin_button_submit").click(onRegularLogin);
        $(".landingPage_loginButton_buttonGoToDashboard").click(showDashBoard);
        $(".landingPage_Carousel_section_chart_mac").dblclick(showDashBoard);
        $(".LandingPageContact_left_box_row_input").blur(checkValidtion);
        $(".landingPage_notHaveProjects_box_button").click(hideErrorMessage);
        $(".landingPage_menuButton").click(toggleMenu);

        $(".landingPage_left_arrrow").click(scrollDown);
        $(".landingPage_privacy_button").click(gotToLogin);

        $("#index_body").scroll(scrollHtml);

        showOrHidLandingPage();
        checkIfShowErrorMessage();
        //checkMixpanel()
        checkIfItsFromIframe();
        showTheRightLogo();
        checkIfItsFromChromeExstension();
        checkIfLogin();
        if (window.index_loadIntercom) {
            window.index_loadIntercom();
        }

        if (location.href.toString().indexOf('#login') != -1 && !localStorage.session) {
            $(".index_extentionPage_box_button").click();
        }
        setInterval(setNewNumber, 2500);
    }

    var hide = false;

    function scrollHtml() {
        var fromTop = $(this).scrollTop();

        if (fromTop > 200 && !hide) {
            hide = true;
            $(".landingPage_left_arrrow").fadeOut();
        } else if (fromTop < 20 && $(window).width() > 950) {
            $(".landingPage_left_arrrow").fadeIn();
        }
    }

    function checkIfLogin() {
        // mixPanelTrack('user bring premmision')
    }

    function showTheRightLogo() {
        var url = location.href.toString();
        // if(url.indexOf('evaluex')>-1){//if its evaluex website
        //   $(".landingPage_logo").show()
        //   $(".landingPage_logo1").hide()
        // }
        // else{// if its superquery website
        $(".landingPage_logo").hide();
        $(".landingPage_logo1").show();
        // }
    }

    function setNewNumber() {
        var randomNumber = Math.floor(Math.random() * 500) + 1;
        startNumber += randomNumber;
        var numberWithComma = startNumber.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        $(".landingPage_companies_number_num").text(numberWithComma);
    }

    function toggleMenu() {
        $(this).toggleClass('landingPage_menuButtonClicked');
        $(".landingPage_menu").toggleClass('landingPage_menuOpen');
        $(".landingPage_login").toggleClass('landingPage_loginActive');
    }

    function openInNewPage() {
        let host = window.location.hostname;
        window.open(`https://${host}/dashboards#referrer=bqconsole`, '_blank');
    }

    function checkForLocalStorageCampaign() {
        let campData = localStorage.getItem('campLogin');

        if (campData !== null && location.href.indexOf('#login1') != -1) {
            let localStorageData = JSON.parse(campData);
            localStorageData.env = 'login from web site';
            localStorage.setItem('campLogin', JSON.stringify(localStorageData));
        }
    }

    function loginFromExtention() {

        checkForLocalStorageCampaign();
        $(".index_extentionPage_box_button-text").text('Please wait ...');
        // mixPanelTrack('click on sing up permission')
        var email = window.app_extentionEmail;

        // api('/goog/userTryToLogin', {email}, 'stage2',function(){
        // },function(){})
        setTimeout(() => {
            gotToLogin();
        }, 1000);
    }

    function closePaymentModal() {
        localStorage.removeItem('paymentMade');
        $("#app").show();
        $("#index_body").hide();
        window.close();
    }

    function checkIfItsFromIframe() {
        if (getQueryParams().referrer == 'bqconsole') { //if Referrer in url from chrome extension, add to localstorage so after login will redirect to bqconsole
            localStorage.referrer = 'bqconsole';
        } else if (getQueryParams().referrer == 'bigqueryAlpha') {
            localStorage.referrer = 'bigqueryAlpha';
        } else if (getQueryParams().code == undefined && getQueryParams().referrer != 'bqconsole') {
            localStorage.referrer = '';
        }
    }

    function checkMixpanel() {
        if (location.href.toString().indexOf('mix=')) {
            var trackName = location.href.toString().split('mix=')[1];
            //  mixpanel.track(trackName)
        }
    }

    function scrollDown() {
        $('html, body').animate({
            scrollTop: $(window).height()
        }, 500);
    }

    function hideErrorMessage() {
        $(".landingPage_notHaveProjects").fadeOut();
    }

    function checkIfShowErrorMessage() {
        var link = location.href.toString();
        if (link.indexOf('userDontHaveProjects') > -1) {
            var email = link.split('=')[1];
            $(".landingPage_notHaveProjects").show();
            $(".landingPage_notHaveProjects_box_text").text("There's no Google BigQuery account assigned to " + email);
        }
    }

    function showDashBoard() {
        location.href = '/bqconsole';
    }

    function onRegularLogin() {
        var email = $(".LandingPageLogin_button_inputEmail").val();
        var password = $(".LandingPageLogin_button_inputPassword").val();
        var machineId = Math.floor((Math.random() * 1000) + 1) + '0' + new Date().getTime();
        var data = {
            userId: email,
            password: password,
            machine: machineId
        };
        $(".LandingPageLogin_button_submit").text('Loading...');
        var url = '/goog/login';
        api(url, data, 'stage2', (res) => {
            localStorage.session = res.session;
            localStorage.machineId = machineId;
            window.location.href = '/bqConsole';
            $(".LandingPageLogin_button_submit").text('Login');
            this.setState({
                buttonLoading: true
            });
        }, (res) => {
            $(".LandingPageLogin_button_submit").text('Login');
            if (res && res.responseJSON && res.responseJSON.ERROR) {
                var errorText = res.responseJSON.ERROR;
            } else {
                var errorText = 'User not exists';
            }
            $(".LandingPageLogin_button_error").text(errorText);
            $(".LandingPageLogin_button_error").fadeIn();
        });
    }

    function showPrivacy() {
        $(".landingPage_privacy").fadeIn();
    }

    function showOrHidLandingPage() { // checking if we need to show or to hide the landing page
        if (localStorage.session || location.href.toString().indexOf('code=') > -1 || location.href.toString().indexOf(
            'linkToken=') > -1 || (location.href.toString().indexOf('bqconsole') > -1 && location.href.toString().indexOf(
                '=bqconsole') == -1)) {
            // index_hideLandingPage()
        } else {
            // index_showLandingPage()
        }
    }

    function index_hideLandingPage() {
        return

        if (location.pathname.toString().toLowerCase() !== '/bqconsole' && location.pathname !== '/dashboards' && !location.href.includes('code') && !location.href.includes('gcp')) {
            location.pathname = '/dashboards';
        }
        else if (location.pathname === '/dashboards') {
            $("#index_body").hide();
        }

        // showLandingPage = false;
        // $("#app").show();
        // $("#index_body").hide();
        // if (document.getElementById('index_progress') && document.getElementById('index_progress').style) {
        //     document.getElementById('index_progress').style.display = 'block';
        // }
        // if (document.getElementById('index_landingPage1') && document.getElementById('index_landingPage1').style) {
        //     document.getElementById('index_landingPage1').style.display = 'none';
        // }
        // //   document.getElementById('index_extentionPage').style.display = 'none'

        // checkHideButton();
    }

    window.index_hideLandingPage = index_hideLandingPage;

    function index_showLandingPage() {
        if (location.pathname !== '/login') {
            location.pathname = '/login';
        }
        // if (location.href.indexOf('#login') != -1 && !localStorage.session) {
        //     $("#index_body").hide();
        //     return;
        // }
        // showLandingPage = true;
        // $("#app").hide();
        // $("#index_body").show();
        // if (document.getElementById('index_progress') && document.getElementById('index_progress').style) {
        //     document.getElementById('index_progress').style.display = 'none';
        // }

        // if (document.getElementById('index_extentionPage') && document.getElementById('index_extentionPage').style) {
        //     document.getElementById('index_extentionPage').style.display = 'block';
        // }

        // checkHideButton();
    }

    window.index_showLandingPage = index_showLandingPage;

    function checkHideButton() {
        if (localStorage.session) {
            $(".landingPage_login").hide();
            $(".landingPage_loginButton").hide();
            $(".landingPage_loginButtonGoToDashboard").show();
        } else {
            $(".landingPage_loginButtonGoToDashboard").hide();
            $(".LandingPageTeam_loginButton").show();
        }
    }

    function checkValidtion() {
        var name = $(".LandingPageContact_left_box_row_inputName").val();
        var email = $.trim($(".LandingPageContact_left_box_row_inputEmail").val());
        var isOk = true;
        if (!validateEmail(email)) {
            $(".LandingPageContact_left_box_error2").fadeIn();
            isOk = false;
        } else {
            $(".LandingPageContact_left_box_error2").fadeOut();
        }
        if (name == 0) {
            $(".LandingPageContact_left_box_error1").fadeIn();
            isOk = false;
        } else {
            $(".LandingPageContact_left_box_error1").fadeOut();
        }
        return isOk;
    }

    function contactUs() {
        var data = {};
        data.fname = $(".LandingPageContact_left_box_row_inputName").val();
        data.email = $.trim($(".LandingPageContact_left_box_row_inputEmail").val());
        data.phone = $(".LandingPageContact_left_box_row_inputPhone").val();
        data.company = $(".LandingPageContact_left_box_row_inputCompany").val();
        data.message = $(".LandingPageContact_left_box_row_inputBig").val();
        if (!checkValidtion()) { //if email or name is not valid
            return;
        }
        $(".LandingPageContact_left_box_row_messageSent").fadeIn();
        $(".LandingPageContact_left_box_row_button").hide();
        setTimeout(() => {
            $(".LandingPageContact_left_box_row_messageSent").hide();
            $(".LandingPageContact_left_box_row_button").fadeIn();
        }, 6000);
        var url = '/goog/registerUser';
        api(url, data, 2, (res) => {
        }, (res) => {
        });
    }

    function showLogin() {
        $(".LandingPageLoginHolder").fadeIn();
    }

    function hideLogin() {
        $(".LandingPageLoginHolder").fadeOut();
    }

    function checkIfClickEnter(e) {
        if (e.which == 13) {
            $(this).parent().find('.landingPage_loginButton_button').click();
        }
    }

    function validateEmail(email) {
        var re =
            /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    }

    function checkIfItsFromChromeExstension() {
        if (location.href.toString().indexOf('referrer=') > -1) {
            //mixPanelTrack('enter to login page')
        }
    }

    function mixPanelTrack(trackName) {
        // mixpanel.track(trackName)
    }

    function login() {
        // mixPanelTrack('click on add to chrome button')
        var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
        var isMobile = $(window).width() < 950;
        var locationString = "https://chrome.google.com/webstore/detail/lfckfngaeoheoppemkocjjebloiamfdc";
        if (isChrome && !isMobile) { // inline-installation for Chrome users.
            chrome.webstore.install(null, function () {
                // mixPanelTrack('exstension confirm install')
            }, function (err) {
                // mixPanelTrack('exstension cancel install')
                if (err.indexOf('Installs can only be initiated by one of the Chrome Web Store') > -1) {
                    location.href = locationString;
                }
                console.error('cannot install chrome: ', err);
            });
        } else { // redirect non-chrome users to a proper page.
            // https://chrome.google.com/webstore/detail/lfckfngaeoheoppemkocjjebloiamfdc
            location.href = locationString;
        }
        return;
        var email = $.trim($(this).parent().find('.landingPage_loginButton_input').val());
        if (!validateEmail(email)) { // if email is not valid
            $(this).parent().parent().find('.landingPage_loginButton_error').fadeIn();
            return;
        }
        $(this).parent().find('.landingPage_loginButton_error').fadeOut();
        $(this).addClass('landingPage_loginButton_buttonLoding');
        $(this).text('Loading...');
        api('/goog/registerUser', {
            email
        }, 2, (res) => {
        }, (res) => {
        });
        showPrivacy();
    }

    function api(api, data, prod, success, error) {
        var url = getUrl(prod);
        if (!data) {
            var data = {};
        }
        if (localStorage.machineId) {
            data.machineId = localStorage['machineId'];
        }
        if (localStorage.session) {
            data.session = localStorage['session'];
        }
        var longUrl = `${url}${api}`;
        var type = getQueryParams().method ? getQueryParams().method : 'post';
        $.ajax({
            url: longUrl,
            type,
            data: (type == 'post') ? JSON.stringify(data) : data,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: (res) => {
                success(res);
            },
            error: (err) => {
                console.log("*******************************");
                console.error(longUrl, type, err, data);
                console.log("*******************************");
                error(err);
            }
        });
    }

    function gotToLogin() {
        if (window.fromExtension) {
            window.sendLoginToExtension()
            return
        }
        console.log("gotToLogin ...");
        var timeout = 50;
        if (getQueryParams().referrer == 'bqconsole') { //if Referrer in url from chrome extension, add to localstorage so after login will redirect to bqconsole
            localStorage.referrer = 'bqconsole';
            timeout = 350;
        } else if (getQueryParams().referrer == 'bigqueryAlpha') {
            localStorage.referrer = 'bigqueryAlpha';
            timeout = 350;
        }

        $(".LandingPageLogin_googleLogin_text, .index_extentionPage_box_button span").text('Loading...');
        var url = "";
        var urlAfter = "";
        if (location.href.toString().indexOf('https://localhost') > -1 || location.href.toString().indexOf(
            'https://localhost') > -1) {
            url = 'https://localhost:8080';
            urlAfter = 'https://localhost:8080';
        } else {
            var url = getUrl("1");
            var urlAfter = getUrl("1");
        }

        let permission = location.href.toString().includes('#loginWithoutPermission') || location.href.toString().includes('#loginKing')
        let apiUrl = ''
        if (permission) {
            apiUrl = `${url}/goog/getRedirectURL?noPermissions=true&nextStepURL=${urlAfter}/goog/saveToken`;
        }
        else {
            apiUrl = `${url}/goog/getRedirectURL?nextStepURL=${urlAfter}/goog/saveToken`;
        }

        setTimeout(() => {
            location.href = apiUrl;
        }, timeout);
    }

    function getUrl(functionSet) {
        if (!functionSet) {
            functionSet = '1';
        } else if (functionSet.length > 1) {
            functionSet = functionSet.substr(functionSet.length - 1, functionSet.length);
        }
        var href = location.href.toString();
        if (getQueryParams().dev == 'true') {
            var url = 'https://localhost:8080';
        } else {
            var env = location.href.toString().substr(0, 12);
            console.log(" envi ", env);
            switch (env) {
                case "https://beta":
                    var url =
                        `https://${(functionSet == '2') ? '7j63uc7g2b' : 'd8louw7zh5'}.execute-api.us-east-1.amazonaws.com/stage${functionSet}`;
                    break;
                case "https://www.":
                case "https://eval":
                    var url = `https://api.evaluex.io/stage1`;
                    if (functionSet == 1) {
                        url = `https://api.evaluex.io/stage1`;
                    } else if (functionSet == 2) {
                        url = `https://api2.evaluex.io/stage2`;
                    } else if (functionSet == 3) {
                        url = `https://api3.evaluex.io/stage3`;
                    } else if (functionSet == 4) {
                        url = `https://api4.evaluex.io/stage4`;
                    } else if (functionSet == 5) {
                        url = `https://api5.evaluex.io/stage5`;
                    }
                    break;
                case "https://supe":
                    var url = `https://api1.superquery.io/stage1`;
                    if (functionSet == 1) {
                        url = `https://api1.superquery.io/stage1`;
                    } else if (functionSet == 2) {
                        url = `https://api2.superquery.io/stage2`;
                    } else if (functionSet == 3) {
                        url = `https://api3.superquery.io/stage3`;
                    } else if (functionSet == 4) {
                        url = `https://api4.superquery.io/stage4`;
                    } else if (functionSet == 5) {
                        url = `https://api5.superquery.io/stage5`;
                    }
                    // var stage2 = 'hheo8mr6ig'
                    // if(functionSet==2){
                    //   var url = `https://${stage2}.execute-api.us-east-1.amazonaws.com/stage${functionSet}`
                    // }else{
                    //   var url = `https://api.evaluex.io/stage1`
                    // }
                    break;
                default:

                    //  var url = `https://${(functionSet=='2')?'b2ddc3wbo8':'s1dg0yjhih'}.execute-api.us-west-1.amazonaws.com/stage${functionSet}`
                    var url = `https://devapi1.evaluex.io/stage1`;
                    if (functionSet == 1) {
                        url = `https://devapi1.evaluex.io/stage1`;
                    } else if (functionSet == 2) {
                        url = `https://devapi2.evaluex.io/stage2`;
                    } else if (functionSet == 3) {
                        url = `https://devapi3.evaluex.io/stage3`;
                    } else if (functionSet == 4) {
                        url = `https://devapi4.evaluex.io/stage4`;
                    } else if (functionSet == 5) {
                        url = `https://devapi5.evaluex.io/stage5`;
                    }

                    break;
            }
        }
        return url;
    }

    function getQueryParams(qs) {
        if (window.location.href.indexOf('#') == -1) {
            return {};
        }
        if (!qs) {
            if (window.location.href.split('#').length) {
                qs = window.location.href.split('#')[1]; // get query string
            } else {
                qs = '';
            }
        }
        qs = qs.split('+').join(' ');
        var params = {},
            tokens,
            re = /[?&]?([^=]+)=([^&]*)/g;
        while (tokens = re.exec(qs)) {
            params[decodeURIComponent(tokens[1])] = decodeURIComponent(tokens[2]);
        }
        return params;
    }
}

if (location.href.toString().indexOf('evaluex.io/install') > -1 || location.href.toString().indexOf(
    'superquery.io/install') > -1) {
    $("#landingPage_loginButton_button1").click();
}


function showLoader(time = 2000) {
    if (document.getElementById('index_progress').style && document.getElementById('index_progress').style) {
        randomWelcomeTips();

        document.getElementById('index_progress').style.display = 'block';

    }
    setTimeout(() => {
        var element = document.getElementById('index_progress');
        element.parentNode.removeChild(element);
    }, time);
}

showLoader(2000);

function handleFontAwesome() {
    let headElement = document.getElementsByTagName('head')[0];
    let linkElement = document.createElement("link");
    linkElement.href = "./doc/font_awesome.css";
    linkElement.rel = "stylesheet";
    linkElement.type = "text/css";

    // let settings = {
    //     "async": true,
    //     "crossDomain": true,
    //     "url": "https://pro.fontawesome.com/releases/v5.8.1/css/all.css",
    //     "method": "GET",
    //     "headers": {
    //     },
    //     "processData": false
    // };
    // try {
    //     $.ajax(settings).done(function (data, status, response) {
    //         if (response.status === 200) {
    //             linkElement.href = "https://pro.fontawesome.com/releases/v5.8.1/css/all.css";
    //             linkElement.rel = "stylesheet";
    //             linkElement.integrity = "sha384-Bx4pytHkyTDy3aJKjGkGoHPt3tvv6zlwwjc3iqN7ktaiEMLDPqLSZYts2OjKcBx1";
    //             linkElement.crossOrigin = "anonymous";
    //         }
    //         headElement.append(linkElement);
    //     });
    // } catch {
        headElement.append(linkElement);
    // }
}
function randomWelcomeTips() {
    const sentences = [
        "Pro Tip: Your queries won't disappear after you leave your screen!",
        "Pro Tip: Click on the <i class='fas fa-chart-bar'></i> icon to instantly visualize your query's result.",
        "Did you know you can download up to 6,000,000 rows to CSV with superQuery?",
        "Pro Tip: Categorize your queries into groups using <i class='fas fa-th'></i> Boards.",
        "Pro Tip: Use variables in your queries to make them dynamic.",
        "Pro Tip: Connect your BI tool to superQuery to run faster queries at a fraction of the cost. Find the <i class='far fa-rocket'></i> icon to set this up.",
        "Pro Tip: Run multiple queries in a single tab by separating your queries with ;",
        "Did you know you can schedule a series of DML statements to execute in a sequence?",
        "Pro Tip: Click on the Visualize toggle to instantly transform all of your query tabs into a single dashboard."
    ];
    const elemId = document.getElementById("index_progress");
    if(elemId !== 'undefined'){
        let elem = document.querySelector('.index_progress_title') ? document.querySelector('.index_progress_title') : null;
        let sentence = sentences[Math.floor(Math.random() * sentences.length)];
        elem.innerHTML = sentence;

    }
}
handleFontAwesome();
