gsap.registerPlugin(ScrollTrigger);

(function ($) {
    /* animation_text
  -------------------------------------------------------------------------*/
    var animation_text = function () {
        if ($(".split-text").length > 0) {
            var st = $(".split-text");
            if (st.length === 0) return;
            gsap.registerPlugin(SplitText, ScrollTrigger);
            st.each(function (index, el) {
                const $el = $(el);
                const $target =
                    $el.find("p, a").length > 0 ? $el.find("p, a")[0] : el;
                const hasClass = $el.hasClass.bind($el);
                const pxl_split = new SplitText($target, {
                    type: "words, chars",
                    lineThreshold: 0.5,
                    linesClass: "split-line",
                });
                let split_type_set = pxl_split.chars;
                gsap.set($target, { perspective: 400 });

                const settings = {
                    scrollTrigger: {
                        trigger: $target,
                        start: "top 86%",
                        once: true,
                    },
                    duration: 0.9,
                    stagger: 0.02,
                    ease: "power3.out",
                };

                if (hasClass("effect-fade")) settings.opacity = 0;

                if (
                    hasClass("split-lines-transform") ||
                    hasClass("split-lines-rotation-x")
                ) {
                    pxl_split.split({
                        type: "lines",
                        lineThreshold: 0.5,
                        linesClass: "split-line",
                    });
                    split_type_set = pxl_split.lines;
                    settings.opacity = 0;
                    settings.stagger = 0.5;
                    if (hasClass("split-lines-rotation-x")) {
                        settings.rotationX = -120;
                        settings.transformOrigin = "top center -50";
                    } else {
                        settings.yPercent = 100;
                        settings.autoAlpha = 0;
                    }
                }

                if (hasClass("split-words-scale")) {
                    pxl_split.split({ type: "words" });
                    split_type_set = pxl_split.words;
                    split_type_set.forEach((elw, index) => {
                        gsap.set(
                            elw,
                            {
                                opacity: 0,
                                scale: index % 2 === 0 ? 0 : 2,
                                force3D: true,
                                duration: 0.1,
                                ease: "power3.out",
                                stagger: 0.02,
                            },
                            index * 0.01
                        );
                    });
                    gsap.to(split_type_set, {
                        scrollTrigger: {
                            trigger: el,
                            start: "top 86%",
                            once: true,
                        },
                        rotateX: "0",
                        scale: 1,
                        opacity: 1,
                    });
                } else if (hasClass("effect-blur-fade")) {
                    pxl_split.split({ type: "words" });
                    split_type_set = pxl_split.words;
                    gsap.fromTo(
                        split_type_set,
                        { opacity: 0, filter: "blur(10px)", y: 20 },
                        {
                            opacity: 1,
                            filter: "blur(0px)",
                            y: 0,
                            duration: 1,
                            stagger: 0.1,
                            ease: "power3.out",
                            scrollTrigger: {
                                trigger: $target,
                                start: "top 86%",
                                toggleActions: "play none none reverse",
                                once: true,
                            },
                        }
                    );
                } else {
                    gsap.from(split_type_set, settings);
                }
            });
        }
    };

    /* scrolling_effect
  -------------------------------------------------------------------------*/
    var scrolling_effect = function () {
        if ($(".scrolling-effect").length > 0) {
            var st = $(".scrolling-effect");
            st.each(function (index, el) {
                var $el = $(el);
                var delay = parseFloat($el.data("delay")) || 0;
                var settings = {
                    scrollTrigger: {
                        trigger: el,
                        scrub: 3,
                        toggleActions: "play none none reverse",
                        start: "30px bottom",
                        end: "bottom bottom",
                        once: true,
                        delay: delay,
                    },
                    duration: 0.8,
                    ease: "power3.out",
                };

                if ($el.hasClass("effectRight")) {
                    settings.opacity = 0;
                    settings.x = "80";
                }
                if ($el.hasClass("effectLeft")) {
                    settings.opacity = 0;
                    settings.x = "-80";
                }
                if ($el.hasClass("effectBottom")) {
                    settings.opacity = 0;
                    settings.y = "20%";
                }
                if ($el.hasClass("effectTop")) {
                    settings.opacity = 0;
                    settings.y = "-80";
                }
                if ($el.hasClass("effectZoomIn")) {
                    settings.opacity = 0;
                    settings.scale = 0.4;
                }

                gsap.from(el, settings);
            });
        }
    };

    /* animateImgItem
    -------------------------------------------------------------------------------------*/
    var animateImgItem = function () {
        const isSmallScreen = window.matchMedia("(max-width: 991px)").matches;

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        const delay =
                            parseFloat(
                                entry.target.getAttribute("data-delay")
                            ) || 0;
                        setTimeout(() => {
                            $(entry.target).addClass("active-animate");
                        }, delay * 1000);
                    }
                });
            },
            {
                threshold: isSmallScreen ? 0.1 : 0.1,
            }
        );

        const elements = $(
            ".tf-animate-1, .tf-animate-2, .tf-animate-3, .tf-animate-4"
        );
        elements.each(function () {
            observer.observe(this);
        });

        const checkVisible = () => {
            elements.each(function () {
                const sectionOffsetTop = $(this).offset().top;
                const sectionHeight = $(this).outerHeight();
                const scrollPosition = $(window).scrollTop();
                const windowHeight = $(window).height();

                if (
                    scrollPosition + windowHeight * 0.9 > sectionOffsetTop &&
                    scrollPosition < sectionOffsetTop + sectionHeight
                ) {
                    const delay = parseFloat($(this).attr("data-delay")) || 0;
                    setTimeout(() => {
                        $(this).addClass("active-animate");
                    }, delay * 1000);
                }
            });
        };

        $(document).ready(checkVisible);
        $(window).on("scroll", checkVisible);
    };

    /* scrollTransform
    -------------------------------------------------------------------------------------*/
    var scrollTransform = function () {
        const scrollTransformElements =
            document.querySelectorAll(".scroll-tranform");
        if (scrollTransformElements.length > 0) {
            scrollTransformElements.forEach(function (element) {
                const direction = element.dataset.direction || "up";
                const distance = element.dataset.distance || "10%";
                let animationProperty;
                switch (direction.toLowerCase()) {
                    case "left":
                        animationProperty = { x: `-${distance}` };
                        break;
                    case "right":
                        animationProperty = { x: `${distance}` };
                        break;
                    case "up":
                        animationProperty = { y: `-${distance}` };
                        break;
                    case "down":
                        animationProperty = { y: `${distance}` };
                        break;
                    default:
                        animationProperty = { y: `-${distance}` };
                }

                gsap.to(element, {
                    ...animationProperty,
                    scrollTrigger: {
                        trigger: element,
                        start: "top center",
                        end: "bottom top",
                        scrub: 2,
                    },
                });
            });
        }
    };

    $(function () {
        animation_text();
        scrolling_effect();
        animateImgItem();
        scrollTransform();
    });
})(jQuery);
