/*!
 * Financial Times Advertising Suite Library
 *
 * Copyright (c) 2015, Financial Times LTD
 * All rights reserved.
 *
 * @author Federico Orru' <federico@buzzler.com>
 *
 */
! function(e, i, t, a) {
	"use strict";

	function n(i) {
		return i = i.substr(0, 1).toUpperCase() + i.substr(1), Math.max(document.documentElement["client" + i], e["inner" + i] || 0)
	}

	function o(e) {
		return "string" == typeof e || e && "object" == typeof e && "[object String]" == Object.prototype.toString.call(e) || !1
	}
	var r = {
			version: "1.1.0",
			testMode: !1,
			mobile: !1,
			dataSource: "",
			itemsPerSlide: 1,
			itemsLimit: null,
			direction: "horizontal",
			coverIsSlide: !1,
			coverDuration: 3,
			copyHeaderOnContent: !1,
			slideChangeDuration: .5,
			slideChangeEasing: "easeOutQuad",
			autoSlide: !0,
			autoSlideInterval: 6,
			autoSlideLimit: 3,
			autoSlideLimitOnMobile: !1,
			pauseAutoSlideOnHover: !0,
			articleHoverAnimation: !1,
			navigationDirectLinks: !1,
			defaultArticleImage: null,
			ellipsis: "...",
			headerEllipsis: !1,
			imageProtocol: "https:",
			phoneBreakPoint: 800,
			randomizeVideo: !1,
			coverSelector: ".cover",
			headerSelector: "header",
			containerSelector: ".content",
			slidesContainerSelector: ".slides",
			slideSelector: ".articles",
			articleSelector: ".article",
			navigationSelector: ".navigation",
			hubLinkSelector: ".coverImage a, .pageTitle a",
			exitClickHandler: function(e, i) {
				Enabler.exitOverride("Default Exit", i)
			},
			hubClickHandler: function(e) {
				Enabler.exitOverride("Hub Exit", e)
			},
			slidesContainerTemplate: function() {
				var e = '<ul class="slides"></ul><nav class="navigation"><ul><li class="prev"><a href="#prev">Previous</a></li><li class="next"><a href="#next">Next</a></li></ul></nav>';
				return e
			},
			navigationLinkTemplate: function(e, i) {
				return '<li class="slideLink index-' + e + (i ? " current" : "") + '"><a href="#' + e + '">Go to Slide #' + e + "</a></li>"
			},
			slideTemplate: function(e) {
				var i = '<li class="slide index-' + e + '" data-index="' + e + '" ><ul class="articles"></ul></li>';
				return i
			},
			articleTemplate: function(e) {
				var i = '<li class="article index-' + e.index + (e.isVideo ? " video" : "") + '" data-index="' + e.index + '"><a class="articleLink" href="' + e.url + '" data-id="' + e.id + '">';
				return e.image && (i += '<div class="image" style="background-image: url(\'' + e.image + "')\"></div>"), i += '<div class="articleContent"><h2 class="articleTitle">' + (e.isVideo ? '<span class="videoLabel">Video</span>' : "") + e.title + '</h2><p class="articleDescription">' + e.description + "</p></div></a></li>"
			}
		},
		l = Array.isArray || function(e) {
			return e && "object" == typeof e && "number" == typeof e.length && "[object Array]" == Object.prototype.toString.call(e)
		},
		s = r.mobile,
		c = r.phoneBreakPoint;
	if ("ftSuiteConfig" in e) {
		"mobile" in ftSuiteConfig && (s = ftSuiteConfig.mobile), "phoneBreakPoint" in ftSuiteConfig && (c = r.phoneBreakPoint);
		var d = s && Math.max(n("width"), n("height")) < c ? 1 : 0;
		for (var u in ftSuiteConfig) u in r && (r[u] = l(ftSuiteConfig[u]) ? ftSuiteConfig[u][d] : ftSuiteConfig[u]);
		ftSuiteConfig.version = r.version
	}
	var f = function() {
		function a(e, t, a) {
			var n = 0 === e.indexOf("http") ? "jsonp" : "json";
			i.ajax({
				url: e,
				dataType: n,
				crossDomain: !0
			}).done(t).fail(a)
		}

		function n(e, i) {
			var a = e.find(".image"),
				n = t.get(a);
			switch (n.duration(.4).easing("easeOutQuad"), i) {
				case "scaleTranslate":
					t.set(a, {
						transformOrigin: "0% 50%"
					}), n.to({
						scale: 1.2,
						z: "0.1px",
						rotate: "0.1deg"
					});
					break;
				case "scale":
					n.to({
						scale: 1.2,
						z: "0.1px",
						rotate: "0.1deg"
					});
					break;
				case "opacity":
					n.to({
						opacity: 1
					})
			}
			return n
		}

		function l() {
			T.on("click", 'a[href^="http"]', function(e) {
				if (!r.testMode) {
					var t = i(this),
						a = t.data("id"),
						n = t.attr("href");
					return r.exitClickHandler(a, n), e.preventDefault(), !1
				}
			}), r.articleHoverAnimation && T.on("mouseenter", r.articleSelector, function(e) {
				var t = i(this),
					a = t.data("animation");
				a || (a = n(t, r.articleHoverAnimation), t.data("animation", a)), a.play()
			}).on("mouseleave", r.articleSelector, function(e) {
				var t = i(this),
					a = t.data("animation");
				a || (a = n(t, r.articleHoverAnimation), t.data("animation", a)), a.reverse()
			}), 2 > C ? O.hide() : O.on("click", "a", function(e) {
				if (!L) {
					r.autoSlideLimit && (r.autoSlideLimit = 0);
					var t, a = i(this),
						n = a.attr("href").substr(1);
					"next" === n ? (n = (x + 1) % C, t = 1) : "prev" === n ? (n = x - 1, 0 > n && (n = C - 1), t = -1) : (n = parseInt(n), t = x > n ? -1 : 1), n != x && h(n, t)
				}
				return e.preventDefault(), !1
			})
		}

		function c() {
			r.autoSlideLimit && r.autoSlideLimit--, h((x + 1) % C, 1)
		}

		function d() {
			k || null !== r.autoSlideLimit && !r.autoSlideLimit || (k = setTimeout(c, 1e3 * r.autoSlideInterval))
		}

		function u() {
			k && (clearTimeout(k), k = null)
		}

		function f() {
			d(), T.on("mouseenter", function() {
				E = !0, u()
			}).on("mouseleave", function() {
				d(), E = !1
			})
		}

		function m() {
			if (C > 1) {
				var e, t, a = O.find(".next");
				for (e = 0; C > e; e++) t = i(r.navigationLinkTemplate(e, e == x)), t.insertBefore(a)
			}
		}

		function g(e) {
			return r.randomizeVideo && Math.random() < .5 ? !0 : !1
		}

		function p(e) {
			var t = null === r.itemsLimit ? e.total : Math.min(r.itemsLimit, e.total);
			C = Math.floor(t / r.itemsPerSlide);
			var a;
			if (!C && t ? (C = 1, a = t) : a = C * r.itemsPerSlide, a) {
				var n, o, l, s, c, d, u, f, p = 0,
					v = 0;
				for (d = 0; a > d; d++) {
					if (d % r.itemsPerSlide === 0 && (v = 0, n = i(r.slideTemplate(p)), o = n.find(r.slideSelector), b.push(n), T.append(n), p++), s = e.pageItems[d], c = r.defaultArticleImage, s.images.length)
						for (u = 0, f = s.images.length; f > u; u++)
							if ("primary" === s.images[u].type) {
								c = s.images[u].url, r.imageProtocol !== !1 && (c = r.imageProtocol + c.substr(c.indexOf("/")));
								break
							}
					l = i(r.articleTemplate({
						index: v,
						id: s.id,
						title: s.title.title,
						url: s.location.uri,
						image: c,
						isVideo: g(s)
					})), o.append(l), v++
				}
				r.navigationDirectLinks && m(), S()
			}
		}

		function v(e) {
			var i = {};
			return i[I] = e, i
		}

		function h(e, i) {
			function a() {
				x = e, L = !1, !E && r.autoSlide && d(), r.navigationDirectLinks && (O.find(".current").removeClass("current"), O.find(".index-" + x).addClass("current"))
			}
			L = !0, u();
			var n;
			n = 1 === i && x > e || -1 === i && e > x ? 1 : Math.abs(e - x);
			var o = t.line();
			if (1 === n) o.add(t.get(b[x]).from(v("0%")).to(v(100 * -i + "%")).duration(r.slideChangeDuration).easing(r.slideChangeEasing), 0).add(t.get(b[e]).from(v(100 * i + "%")).to(v("0%")).duration(r.slideChangeDuration).easing(r.slideChangeEasing), 0).on("complete", a).play();
			else {
				var l, s = e + i,
					c = 0,
					f = -i * n * 100,
					m = 100 * i;
				for (l = x; l != s; l += i) o.add(t.get(b[l]).from(v(c + "%")).to(v(f + "%")).duration(r.slideChangeDuration).easing(r.slideChangeEasing), 0), c += m, f += m;
				o.on("complete", a).play()
			}
		}

		function S() {
			l(), i(".loading").removeClass("loading");
			var e = function() {
				r.autoSlide && f()
			};
			if (r.coverIsSlide ? t.get(D).delay(r.coverDuration).to(v("-100%")).duration(r.slideChangeDuration).easing(r.slideChangeEasing).on("complete", e).play() : e(), r.ellipsis !== !1) {
				var a = "+" + r.ellipsis,
					n = a.length;
				T.find(".articleContent").dotdotdot({
					ellipsis: a,
					wrap: "word",
					fallbackToLetter: !1,
					after: null,
					watch: r.mobile ? "window" : !1,
					height: null,
					tolerance: 2,
					callback: function(e) {
						if (e) {
							var t, o, r, l, s = i(this),
								c = s.find(".articleTitle"),
								d = c.text();
							if (t = d.lastIndexOf(a) === d.length - n ? c : s.find(".articleDescription"), o = t.html())
								for (l = a.substr(1), o = o.substr(0, o.length - n), t.html(o + '<span class="ellipsis">' + l + "</span>"); this.scrollHeight > this.clientHeight + 2;) r = o.split(/\s+/), r.pop(), o = r.join(" "), t.html(o + '<span class="ellipsis">' + a.substr(1) + "</span>")
						}
					},
					lastCharacter: {
						remove: [" ", ",", ";", ".", "!", "?"],
						noEllipsis: []
					}
				})
			}
		}!s || e.Origami && e.Origami["o-ads-embed"] || i.ajax({
			url: "http://build.origami.ft.com/v2/bundles/js?modules=o-ads-embed",
			dataType: "script",
			cache: !0
		}).done(function(i, t) {
			e.Origami["o-ads-embed"].init()
		}).fail(function(e, i, t) {
			console.log("Error including script"), console.log("Text status: ", i), console.error(t)
		}), t.defaultTimeUnit = "s";
		var b = [],
			C = 0,
			x = 0,
			L = !1,
			k = null,
			E = !1,
			y = i(r.containerSelector);
		if (!y.length) throw 'Container with selector "' + r.containerSelector + '" not found"';
		y.append(r.slidesContainerTemplate());
		var T = y.find(r.slidesContainerSelector),
			O = i(r.navigationSelector),
			D = i(r.coverSelector);
		if (i("body").on("click", r.hubLinkSelector, function(e) {
				return r.hubClickHandler(i(this).attr("href")), e.preventDefault(), !1
			}), r.headerEllipsis !== !1 && D.find(r.headerSelector).dotdotdot({
				ellipsis: r.headerEllipsis,
				wrap: "word",
				fallbackToLetter: !0,
				after: null,
				watch: r.mobile ? "window" : !1,
				height: null,
				tolerance: 2,
				lastCharacter: {
					remove: [" ", ",", ";", ".", "!", "?"],
					noEllipsis: []
				}
			}), r.copyHeaderOnContent) {
			var w = D.find(r.headerSelector).clone();
			y.prepend(w)
		}
		r.direction = "v" === r.direction.charAt(0).toLowerCase() ? "vertical" : "horizontal";
		var I = "horizontal" === r.direction ? "translateX" : "translateY";
		if (!r.defaultArticleImage) {
			var A = i(".coverImage").css("background-image");
			"none" !== A && (r.defaultArticleImage = A.slice(4, -1).replace(/["']/g, ""))
		}
		if (null !== r.autoSlideLimit && (!r.autoSlideLimitOnMobile && s ? r.autoSlideLimit = null : r.autoSlideLimit -= r.coverIsSlide ? 2 : 1), o(r.dataSource)) {
			if (0 === r.dataSource.indexOf("//")) {
				var H = 0 === document.location.href.indexOf("https:") ? "https:" : "http:";
				r.dataSource = H + r.dataSource
			}
			a(r.dataSource, p, function(e, i, t) {
				console.log("Error in remote call:"), console.log("Text status: ", i), console.error(t)
			})
		} else p(r.dataSource)
	};
	r.testMode ? f() : Enabler.isInitialized() ? f() : Enabler.addEventListener(studio.events.StudioEvent.INIT, function() {
		Enabler.isPageLoaded() ? f() : Enabler.addEventListener(studio.events.StudioEvent.PAGE_LOADED, f)
	})
}(window, require("jquery"), require("tweene/velocity"));
//# sourceMappingURL=ft-suite.js.map