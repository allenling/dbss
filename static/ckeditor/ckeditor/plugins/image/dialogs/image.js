/*
 Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 For licensing, see LICENSE.md or http://ckeditor.com/license
*/
(function () {
    var r = function (c, j) {
        function r() {
            var a = arguments,
                b = this.getContentElement("advanced", "txtdlgGenStyle");
            b && b.commit.apply(b, a);
            this.foreach(function (b) {
                b.commit && "txtdlgGenStyle" != b.id && b.commit.apply(b, a)
            })
        }

        function i(a) {
            if (!s) {
                s = 1;
                var b = this.getDialog(),
                    d = b.imageElement;
                if (d) {
                    this.commit(f, d);
                    for (var a = [].concat(a), e = a.length, c, g = 0; g < e; g++)(c = b.getContentElement.apply(b, a[g].split(":"))) && c.setup(f, d)
                }
                s = 0
            }
        }
        var f = 1,
            k = /^\s*(\d+)((px)|\%)?\s*$/i,
            v = /(^\s*(\d+)((px)|\%)?\s*$)|^$/i,
            o = /^\d+px$/,
            w = function () {
                var a = this.getValue(),
                    b = this.getDialog(),
                    d = a.match(k);
                d && ("%" == d[2] && l(b, !1), a = d[1]);
                b.lockRatio && (d = b.originalElement, "true" == d.getCustomData("isReady") && ("txtHeight" == this.id ? (a && "0" != a && (a = Math.round(d.$.width * (a / d.$.height))), isNaN(a) || b.setValueOf("info", "txtWidth", a)) : (a && "0" != a && (a = Math.round(d.$.height * (a / d.$.width))), isNaN(a) || b.setValueOf("info", "txtHeight", a))));
                g(b)
            }, g = function (a) {
                if (!a.originalElement || !a.preview) return 1;
                a.commitContent(4, a.preview);
                return 0
            }, s, l = function (a,
                b) {
                if (!a.getContentElement("info", "ratioLock")) return null;
                var d = a.originalElement;
                if (!d) return null;
                if ("check" == b) {
                    if (!a.userlockRatio && "true" == d.getCustomData("isReady")) {
                        var e = a.getValueOf("info", "txtWidth"),
                            c = a.getValueOf("info", "txtHeight"),
                            d = 1E3 * d.$.width / d.$.height,
                            f = 1E3 * e / c;
                        a.lockRatio = !1;
                        !e && !c ? a.lockRatio = !0 : !isNaN(d) && !isNaN(f) && Math.round(d) == Math.round(f) && (a.lockRatio = !0)
                    }
                } else void 0 != b ? a.lockRatio = b : (a.userlockRatio = 1, a.lockRatio = !a.lockRatio);
                e = CKEDITOR.document.getById(p);
                a.lockRatio ?
                    e.removeClass("cke_btn_unlocked") : e.addClass("cke_btn_unlocked");
                e.setAttribute("aria-checked", a.lockRatio);
                CKEDITOR.env.hc && e.getChild(0).setHtml(a.lockRatio ? CKEDITOR.env.ie ? "■" : "▣" : CKEDITOR.env.ie ? "□" : "▢");
                return a.lockRatio
            }, x = function (a) {
                var b = a.originalElement;
                if ("true" == b.getCustomData("isReady")) {
                    var d = a.getContentElement("info", "txtWidth"),
                        e = a.getContentElement("info", "txtHeight");
                    d && d.setValue(b.$.width);
                    e && e.setValue(b.$.height)
                }
                g(a)
            }, y = function (a, b) {
                function d(a, b) {
                    var d = a.match(k);
                    return d ?
                        ("%" == d[2] && (d[1] += "%", l(e, !1)), d[1]) : b
                }
                if (a == f) {
                    var e = this.getDialog(),
                        c = "",
                        g = "txtWidth" == this.id ? "width" : "height",
                        h = b.getAttribute(g);
                    h && (c = d(h, c));
                    c = d(b.getStyle(g), c);
                    this.setValue(c)
                }
            }, t, q = function () {
                var a = this.originalElement;
                a.setCustomData("isReady", "true");
                a.removeListener("load", q);
                a.removeListener("error", h);
                a.removeListener("abort", h);
                this.dontResetSize || x(this);
                this.firstLoad && CKEDITOR.tools.setTimeout(function () {
                        l(this, "check")
                    },
                    0, this);
                this.dontResetSize = this.firstLoad = !1
            }, h = function () {
                var a = this.originalElement;
                a.removeListener("load", q);
                a.removeListener("error", h);
                a.removeListener("abort", h);
                a = CKEDITOR.getUrl(CKEDITOR.plugins.get("image").path + "images/noimage.png");
                this.preview && this.preview.setAttribute("src", a);
                CKEDITOR.document.getById(m).setStyle("display", "none");
                l(this, !1)
            }, n = function (a) {
                return CKEDITOR.tools.getNextId() + "_" + a
            }, p = n("btnLockSizes"),
            u = n("btnResetSize"),
            m = n("ImagePreviewLoader"),
            A = n("previewLink"),
            z = n("previewImage");
        return {
            title: c.lang.image["image" == j ? "title" : "titleButton"],
            minWidth: 500,
            minHeight: 130,
            onShow: function () {
                this.linkEditMode = this.imageEditMode = this.linkElement = this.imageElement = !1;
                this.lockRatio = !0;
                this.userlockRatio = 0;
                this.dontResetSize = !1;
                this.firstLoad = !0;
                this.addLink = !1;
                var a = this.getParentEditor(),
                    b = a.getSelection(),
                    d = (b = b && b.getSelectedElement()) && a.elementPath(b).contains("a", 1);
                t = new CKEDITOR.dom.element("img", a.document);
                this.preview = CKEDITOR.document.getById(z);
                this.originalElement = a.document.createElement("img");
                this.originalElement.setAttribute("alt", "");
                this.originalElement.setCustomData("isReady", "false");
                if (d) {
                    this.linkElement = d;
                    this.linkEditMode = !0;
                    var c = d.getChildren();
                    if (1 == c.count()) {
                        var g = c.getItem(0).getName();
                        if ("img" == g || "input" == g) this.imageElement = c.getItem(0), "img" == this.imageElement.getName() ? this.imageEditMode = "img" : "input" == this.imageElement.getName() && (this.imageEditMode = "input")
                    }
                    "image" == j &&
                        this.setupContent(2, d)
                }
                if (b && "img" == b.getName() && !b.data("cke-realelement") || b && "input" == b.getName() && "image" == b.getAttribute("type")) this.imageEditMode = b.getName(), this.imageElement = b;
                this.imageEditMode ? (this.cleanImageElement = this.imageElement, this.imageElement = this.cleanImageElement.clone(!0, !0), this.setupContent(f, this.imageElement)) : this.imageElement = a.document.createElement("img");
                l(this, !0);
            },
            onOk: function () {
                if (this.imageEditMode) {
                    var a = this.imageEditMode;
                    "image" == j && "input" == a && confirm(c.lang.image.button2Img) ? (this.imageElement = c.document.createElement("img"), this.imageElement.setAttribute("alt", ""), c.insertElement(this.imageElement)) : "image" != j && "img" == a && confirm(c.lang.image.img2Button) ? (this.imageElement = c.document.createElement("input"), this.imageElement.setAttributes({
                        type: "image",
                        alt: ""
                    }), c.insertElement(this.imageElement)) : (this.imageElement = this.cleanImageElement, delete this.cleanImageElement)
                } else "image" ==
                    j ? this.imageElement = c.document.createElement("img") : (this.imageElement = c.document.createElement("input"), this.imageElement.setAttribute("type", "image")), this.imageElement.setAttribute("alt", "");
                this.linkEditMode || (this.linkElement = c.document.createElement("a"));
                this.commitContent(f, this.imageElement);
                this.commitContent(2, this.linkElement);
                this.imageElement.getAttribute("style") || this.imageElement.removeAttribute("style");
                this.imageEditMode ? !this.linkEditMode && this.addLink ? (c.insertElement(this.linkElement),
                    this.imageElement.appendTo(this.linkElement)) : this.linkEditMode && !this.addLink && (c.getSelection().selectElement(this.linkElement), c.insertElement(this.imageElement)) : this.addLink ? this.linkEditMode ? c.insertElement(this.imageElement) : (c.insertElement(this.linkElement), this.linkElement.append(this.imageElement, !1)) : c.insertElement(this.imageElement)
            },
            onLoad: function () {
                "image" != j && this.hidePage("Link");
                var a = this._.element.getDocument();
                this.getContentElement("info", "ratioLock") && (this.addFocusable(a.getById(u),
                    5), this.addFocusable(a.getById(p), 5));
                this.commitContent = r
            },
            onHide: function () {
                this.preview && this.commitContent(8, this.preview);
                this.originalElement && (this.originalElement.removeListener("load", q), this.originalElement.removeListener("error", h), this.originalElement.removeListener("abort", h), this.originalElement.remove(), this.originalElement = !1);
                delete this.imageElement
            },
            contents: [{
                id: "info",
                label: c.lang.image.infoTab,
                accessKey: "I",
                elements: [{
                    type: "vbox",
                    padding: 0,
                    children: [{
                        type: "hbox",
                        widths: ["100px",
                        ],
                        align: "right",
                        children: [{
                            id: "txtUrl",
                            type: "text",
                            label: c.lang.common.url,
                            required: !0,
                            onChange: function () {
                                var a = this.getDialog(),
                                    b = this.getValue();
                                if (0 < b.length) {
                                    var a = this.getDialog(),
                                        d = a.originalElement;
                                    d.setCustomData("isReady", "false");
                                    var c = CKEDITOR.document.getById(m);
                                    c && c.setStyle("display", "");
                                    d.on("load", q, a);
                                    d.on("error", h, a);
                                    d.on("abort", h, a);
                                    d.setAttribute("src", b);
                                    t.setAttribute("src", b);
                                    g(a)
                                } else a.preview &&
                                    (a.preview.removeAttribute("src"), a.preview.setStyle("display", "none"))
                            },
                            setup: function (a, b) {
                                if (a == f) {
                                    var d = b.data("cke-saved-src") || b.getAttribute("src");
                                    this.getDialog().dontResetSize = !0;
                                    this.setValue(d);
                                    this.setInitValue()
                                }
                            },
                            commit: function (a, b) {
                                a == f && (this.getValue() || this.isChanged()) ? (b.data("cke-saved-src", this.getValue()), b.setAttribute("src", this.getValue())) : 8 == a && (b.setAttribute("src", ""), b.removeAttribute("src"))
                            },
                            validate: CKEDITOR.dialog.validate.notEmpty(c.lang.image.urlMissing)
                        }]
                    }]
                }]
            },{
                id: "Upload",
                hidden: !0,
                filebrowser: "uploadButton",
                label: c.lang.image.upload,
                elements: [{
                    type: "file",
                    id: "upload",
                    label: c.lang.image.btnUpload,
                    style: "height:40px",
                    size: 38
                }, {
                    type: "fileButton",
                    id: "uploadButton",
                    filebrowser: "info:txtUrl",
                    label: c.lang.image.btnUpload,
                    "for": ["Upload", "upload"]
                }]
            }]
        }
    };
    CKEDITOR.dialog.add("image", function (c) {
        return r(c, "image")
    });
    CKEDITOR.dialog.add("imagebutton", function (c) {
        return r(c, "imagebutton")
    })
})();
