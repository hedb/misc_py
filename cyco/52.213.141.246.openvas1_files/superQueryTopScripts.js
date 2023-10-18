function showLocalStorageError() {
    setTimeout(() => {
        openModal('localstorageMessage');
    }, 4000);
}

function isLocalStorageAvailable() {
    try {
        localStorage.setItem('test', true);
        localStorage.removeItem('test');
        return true;
    } catch (err) {
        return false;
    }
}
if (!isLocalStorageAvailable()) {
    showLocalStorageError();
}

function getQueryParams(qs) {
    if (window.location.href.indexOf('&') == -1) {
        return {}
    }

    if (!qs) {
        if (window.location.href.split('&').length) {
            qs = window.location.href.split('&')[1]; // get query string
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

let link = window.location.toString()
if ((window.location.href.search('internal=true') > -1 || window.location.href.search('deleteWidgets=true') > -1) /*&& window.location.href.search('#') > -1*/) {
    localStorage.clear()
    const params = this.getQueryParams(window.location.href.split('?')[1])
    localStorage.session = params.session ? params.session : localStorage.session;
    localStorage.Dashboard_tab = 'dashboards';
    localStorage.Dashboard_id = params.dashboardId ? params.dashboardId : localStorage.Dashboard_id;
    localStorage.Dashboard_editMode = false;
} else if (location.href.toString().indexOf('#login') != -1 && !localStorage.session) {
    $(".index_extentionPage_box_button").click()
}
else if (!localStorage.session && link && link.indexOf('referrer') === -1 && link.indexOf('camp=') === -1 && link.indexOf('code') === -1 && link.indexOf('linkToken') === -1 && link.indexOf('dev.evaluex.io') === -1 && link.indexOf('#login') === -1 && link.indexOf('#fromMobile') === -1 && link.indexOf('localhost') === -1 && link.indexOf('gcp=') === -1) {
    location.href = 'https://web.superquery.io';
    // if (location.pathname !== '/login') {
    //     console.log('2');
    //     location.href = 'https://superquery.io/login' //TODO remove HACK
    // }
} else if ((window.location.pathname == '/' || window.location.pathname == '') && link && link.indexOf('code') === -1 && link.indexOf('camp=') == -1 && link.indexOf('?gcp=') == -1 && localStorage.session) {
    window.location.href = '/dashboards';
}

/*if(window.location.href.search('https://evaluex.io') > -1 && !localStorage.session){
  window.location = 'https://superquery.io'
}
else*/
if (window.location.href.search(`${window.location.host.toString()}/beta`) > -1) { //if user want to go to the beta site
    window.location = '/doc/beta.doc.html'
}




var newUrl = window.location.href.replace("https:\/\/www.evaluex.io", "https://evaluex.io").replace(
    "https:\/\/www.superquery.io", "https://superquery.io");

if (newUrl != window.location.href) {
    window.location.href = newUrl
}

if (location.href.toString().indexOf('localhost/e1') > -1 || location.href.toString().indexOf('evaluex.io/e1') > -1 || location.href.toString().indexOf('superquery.io/e1') > -1) {
    location.href = 'https://chrome.google.com/webstore/detail/superquery-google-bigquer/lfckfngaeoheoppemkocjjebloiamfdc?utm_source=chrome-ntp-icon'
}
else if (location.href.toString().indexOf('localhost/e2') > -1 || location.href.toString().indexOf('evaluex.io/e2') > -1 || location.href.toString().indexOf('superquery.io/e2') > -1) {
    location.href = 'https://chrome.google.com/webstore/detail/superquery-bigquery-optim/lfckfngaeoheoppemkocjjebloiamfdc?utm_source=chrome-ntp-icon'
}

// Set to false if opt-in required
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
    trackcmp.src = '//trackcmp.net/visit?actid=1000048128&e='+encodeURIComponent(trackcmp_email)+'&r='+encodeURIComponent(document.referrer)+'&u='+encodeURIComponent(window.location.href);
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
