(window.webpackJsonp=window.webpackJsonp||[]).push([["o-typography"],{"1891e3a9":function(t,e,o){"use strict";o.r(e);var n=o("1a2bc167"),a=o.n(n);function i(t,e){for(var o=0;o<e.length;o++){var n=e[o];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(t,n.key,n)}}var s=function(){function t(e,o){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t),this.typographyEl=e,this.fontLoadingPrefix="o-typography--loading-",this.opts=o||t.getOptions(e),void 0===this.opts.loadOnInit&&(this.opts.loadOnInit=!0),void 0===this.opts.rejectOnFontLoadFailure&&(this.opts.rejectOnFontLoadFailure=!1),this.opts=t.checkOptions(this.opts),this.hasRun=!1,this.fontConfigs=[{family:"FinancierDisplayWeb",weight:"normal",label:"display"},{family:"MetricWeb",weight:"normal",label:"sans"},{family:"MetricWeb",weight:600,label:"sans-bold"},{family:"FinancierDisplayWeb",weight:700,label:"display-bold"}],this.opts.loadOnInit&&this.loadFonts()}var e,o,n;return e=t,n=[{key:"getOptions",value:function(t){var e=Object(t.dataset);return Object.keys(e).reduce((function(t,o){if("oComponent"===o)return t;var n=o.replace(/^oTypography(\w)(\w+)$/,(function(t,e,o){return e.toLowerCase()+o}));try{t[n]=JSON.parse(e[o].replace(/\'/g,'"'))}catch(a){t[n]=e[o]}return t}),{})}},{key:"checkOptions",value:function(t){return t.fontLoadedCookieName||(t.fontLoadedCookieName="o-typography-fonts-loaded"),t}},{key:"init",value:function(e,o){if(e||(e=document.documentElement),e instanceof HTMLElement||(e=document.querySelector(e)),e instanceof HTMLElement&&e.matches("[data-o-component=o-typography]"))return new t(e,o)}}],(o=[{key:"checkFontsLoaded",value:function(){return new RegExp("(^|s)".concat(this.opts.fontLoadedCookieName,"=1(;|$)")).test(document.cookie)}},{key:"setCookie",value:function(){var t=/.ft.com$/.test(location.hostname)?".ft.com":location.hostname;document.cookie="".concat(this.opts.fontLoadedCookieName,"=1;domain=").concat(t,";path=/;max-age=").concat(604800)}},{key:"removeLoadingClasses",value:function(){var t=this;this.fontConfigs.forEach((function(e){t.typographyEl.classList.remove("".concat(t.fontLoadingPrefix).concat(e.label))}))}},{key:"loadFonts",value:function(){var t=this;if(this.hasRun)return Promise.resolve();if(this.checkFontsLoaded())return this.removeLoadingClasses(),this.setCookie(),this.hasRun=!0,Promise.resolve();var e=this.fontConfigs.map((function(e){return new a.a(e.family,{weight:e.weight}).load().then((function(){t.typographyEl.classList.remove("".concat(t.fontLoadingPrefix).concat(e.label))}))}));return Promise.all(e).then((function(){t.setCookie(),t.hasRun=!0})).catch((function(e){if(t.opts.rejectOnFontLoadFailure)throw e}))}}])&&i(e.prototype,o),n&&i(e,n),t}();document.addEventListener("o.DOMContentLoaded",(function t(){s.init(),document.removeEventListener("o.DOMContentLoaded",t)}));e.default=s}}]);
//# sourceMappingURL=o-typography.40be387e4e4a.bundle.js.map