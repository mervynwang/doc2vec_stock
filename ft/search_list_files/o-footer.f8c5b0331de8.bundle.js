(window.webpackJsonp=window.webpackJsonp||[]).push([["o-footer"],{"7d50df06":function(t,e,o){"use strict";o.r(e);var n=o("c8f94c3a"),r=o("e1e3ba65"),a=o("922a4198");function u(t,e){for(var o=0;o<e.length;o++){var n=e[o];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(t,n.key,n)}}var i=["default","XS","S"],l=function(){function t(e){var o=this;!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t),e?"string"==typeof e&&(e=document.querySelector(e)):e=document.querySelector('[data-o-component="o-footer"]'),this.footerEl=e,function(t){a.default.listenTo("resize");var e=r.default.getCurrentLayout();document.body.addEventListener("oViewport.resize",(function(){var o=r.default.getCurrentLayout();o!==e&&(t(o),e=o)})),t(e)}((function(e){var n=t.shouldCollapse(e);return n&&!o._toggles?o.setup():!n&&o._toggles?o.destroy():void 0})),this.footerEl.removeAttribute("data-o-footer--no-js"),this.footerEl.setAttribute("data-o-footer--js","")}var e,o,l;return e=t,l=[{key:"shouldCollapse",value:function(t){return-1!==i.indexOf(t)}},{key:"init",value:function(e){e?"string"==typeof e&&(e=document.querySelector(e)):e=document.body;var o=e.querySelector('[data-o-component="o-footer"]');if(o)return new t(o)}},{key:"collapsibleBreakpoints",get:function(){return i}}],(o=[{key:"setup",value:function(){var t=this;this._toggles=[];var e=this.footerEl.querySelectorAll("[aria-controls]");Array.prototype.forEach.call(e,(function(e){var o=document.getElementById(e.getAttribute("aria-controls"));e.setAttribute("role","button"),e.setAttribute("tabindex","0"),t._toggles.push(new n.default(e,{target:o}))}))}},{key:"destroy",value:function(){this._toggles.forEach((function(t){return t.destroy()})),this._toggles=null}}])&&u(e.prototype,o),l&&u(e,l),t}();document.addEventListener("o.DOMContentLoaded",(function t(){l.init(),document.removeEventListener("o.DOMContentLoaded",t)}));e.default=l}}]);
//# sourceMappingURL=o-footer.f8c5b0331de8.bundle.js.map