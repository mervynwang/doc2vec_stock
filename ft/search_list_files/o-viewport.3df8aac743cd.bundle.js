(window.webpackJsonp=window.webpackJsonp||[]).push([["o-viewport"],{"922a4198":function(t,i,e){"use strict";e.r(i);var n,o=e("b7c00496");function r(t){return t?document.documentElement.clientHeight:Math.max(document.documentElement.clientHeight,window.innerHeight||0)}function l(t){return t?document.documentElement.clientWidth:Math.max(document.documentElement.clientWidth,window.innerWidth||0)}var c={debug:function(){n=!0},broadcast:function(t,i,e){e=e||document.body,n&&console.log("o-viewport",t,i),e.dispatchEvent(new CustomEvent("oViewport."+t,{detail:i,bubbles:!0}))},getWidth:l,getHeight:r,getSize:function(t){return{height:r(t),width:l(t)}},getScrollPosition:function(){return{height:document.body.scrollHeight,width:document.body.scrollWidth,left:window.pageXOffset||window.scrollX,top:window.pageYOffset||window.scrollY}},getVisibility:function(){return document.hidden},getOrientation:function(){var t=window.screen.orientation;return t?"string"==typeof t?t.split("-")[0]:t.type.split("-")[0]:window.matchMedia?window.matchMedia("(orientation: portrait)").matches?"portrait":"landscape":r()>=l()?"portrait":"landscape"},debounce:o.debounce,throttle:o.throttle},a=c.throttle,d=c.debounce,s={},u={resize:100,orientation:100,visibility:100,scroll:100};i.default={debug:function(){c.debug()},listenTo:function(t){"resize"!==t&&"all"!==t||function(){if(!s.resize){var t=d((function(t){c.broadcast("resize",{viewport:c.getSize(),originalEvent:t})}),u.resize);window.addEventListener("resize",t),s.resize={eventType:"resize",handler:t}}}(),"scroll"!==t&&"all"!==t||function(){if(!s.scroll){var t=a((function(t){var i=c.getScrollPosition();c.broadcast("scroll",{viewport:c.getSize(),scrollHeight:i.height,scrollLeft:i.left,scrollTop:i.top,scrollWidth:i.width,originalEvent:t})}),u.scroll);window.addEventListener("scroll",t),s.scroll={eventType:"scroll",handler:t}}}(),"orientation"!==t&&"all"!==t||function(){if(!s.orientation){var t=d((function(t){c.broadcast("orientation",{viewport:c.getSize(),orientation:c.getOrientation(),originalEvent:t})}),u.orientation);window.addEventListener("orientationchange",t),s.orientation={eventType:"orientationchange",handler:t}}}(),"visibility"!==t&&"all"!==t||function(){if(!s.visibility){var t=d((function(t){c.broadcast("visibility",{hidden:c.getVisibility(),originalEvent:t})}),u.visibility);window.addEventListener("visibilitychange",t),s.visibility={eventType:"visibilitychange",handler:t}}}()},stopListeningTo:function t(i){"all"===i?Object.keys(s).forEach(t):s[i]&&(window.removeEventListener(s[i].eventType,s[i].handler),delete s[i])},setThrottleInterval:function t(i,e){"number"==typeof arguments[0]?(t("scroll",arguments[0]),t("resize",arguments[1]),t("orientation",arguments[2]),t("visibility",arguments[3])):e&&(u[i]=e)},getOrientation:c.getOrientation,getSize:c.getSize,getScrollPosition:c.getScrollPosition,getVisibility:c.getVisibility}}}]);
//# sourceMappingURL=o-viewport.3df8aac743cd.bundle.js.map