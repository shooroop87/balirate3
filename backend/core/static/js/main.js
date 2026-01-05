/**
 
 * preventDefault
 * headerFixed
 * handleFooter
 * spliting
 * effect_button
 * loadProduct
 * showform
 * hoverTabs
 * infiniteslide
 * showInput
 * wishList
 * fillterIso
 * tabSlide
 * video
 * hoverActive
 * oneNavOnePage
 * sendmail
 * slideBarPrivacy
 * goTop
 
**/

(function ($) {
    ("use strict");

    /* preventDefault
  -------------------------------------------------------------------------*/
    const preventDefault = () => {
        $(".link-no-action").on("click", function (e) {
            e.preventDefault();
        });
    };

    /* header_sticky
  -------------------------------------------------------------------------------------*/
    const headerFixed = function () {
        let lastScrollTop = 0;
        const delta = 10;
        const $header = $(".header-sticky");
        let navbarHeight = $header.outerHeight();

        let resizeTimeout;
        $(window).on("resize", function () {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(function () {
                navbarHeight = $header.outerHeight();
            }, 100);
        });
        $(window).on("scroll", function () {
            let scrollTop = $(this).scrollTop();

            if (scrollTop < 350) {
                $header.removeClass("is-sticky");
                return;
            }

            if (scrollTop > lastScrollTop + delta) {
                $header.removeClass("is-sticky");
                $(".sticky-top").css("top", "0");
            } else if (scrollTop < lastScrollTop - delta) {
                $header.addClass("is-sticky");
                $(".sticky-top").css("top", `${15 + navbarHeight}px`);
            }

            lastScrollTop = scrollTop;
        });
    };

    /* headerFixed
  -------------------------------------------------------------------------------------*/
    const headerFixed2 = () => {
        const $header = $(".header-fixed");
        if (!$header.length) return;
        $(window).on("scroll", () => {
            $header.toggleClass("is-fixed", $(window).scrollTop() >= 350);
        });
    };

    /* footer accordion
  -------------------------------------------------------------------------*/
    var handleFooter = function () {
        var footerAccordion = function () {
            var args = { duration: 250 };
            $(".footer-heading-mobile").on("click", function () {
                $(this).parent(".footer-col-block").toggleClass("open");
                if (!$(this).parent(".footer-col-block").is(".open")) {
                    $(this).next().slideUp(args);
                } else {
                    $(this).next().slideDown(args);
                }
            });
        };
        function handleAccordion() {
            if (matchMedia("only screen and (max-width: 767px)").matches) {
                if (
                    !$(".footer-heading-mobile").data("accordion-initialized")
                ) {
                    footerAccordion();
                    $(".footer-heading-mobile").data(
                        "accordion-initialized",
                        true
                    );
                }
            } else {
                $(".footer-heading-mobile").off("click");
                $(".footer-heading-mobile")
                    .parent(".footer-col-block")
                    .removeClass("open");
                $(".footer-heading-mobile").next().removeAttr("style");
                $(".footer-heading-mobile").data(
                    "accordion-initialized",
                    false
                );
            }
        }
        handleAccordion();
        window.addEventListener("resize", function () {
            handleAccordion();
        });
    };

    /* spliting
  -------------------------------------------------------------------------*/
    const spliting = () => {
        if ($(".splitting").length) {
            Splitting();
        }
    };

    /* effect_button
  -------------------------------------------------------------------------*/
    var effect_button = () => {
        $(".tf-btn").each(function () {
            var button_width = $(this).outerWidth();
            $(this).css("--button-width", button_width + "px");
        });
        $(".tf-btn")
            .on("mouseenter", function (e) {
                var parentOffset = $(this).offset(),
                    relX = e.pageX - parentOffset.left,
                    relY = e.pageY - parentOffset.top;
                $(this).find(".bg-effect").css({ top: relY, left: relX });
            })
            .on("mouseout", function (e) {
                var parentOffset = $(this).offset(),
                    relX = e.pageX - parentOffset.left,
                    relY = e.pageY - parentOffset.top;
                $(this).find(".bg-effect").css({ top: relY, left: relX });
            });
    };

    /* Loading product 
  -------------------------------------------------------------------------------------*/
    var loadProduct = function () {
        const gridInitialItems = 9;
        const listInitialItems = 4;
        const gridItemsPerPage = 3;
        const listItemsPerPage = 2;

        let listItemsDisplayed = listInitialItems;
        let gridItemsDisplayed = gridInitialItems;
        let scrollTimeout;

        function hideExtraItems(layout, itemsDisplayed) {
            layout.find(".loadItem").each(function (index) {
                if (index >= itemsDisplayed) {
                    $(this).addClass("hidden");
                }
            });
            if (layout.is("#listLayout")) updateLastVisible(layout);
        }

        function showMoreItems(layout, itemsPerPage, itemsDisplayed) {
            const hiddenItems = layout.find(".loadItem.hidden");

            setTimeout(function () {
                hiddenItems.slice(0, itemsPerPage).removeClass("hidden");
                if (layout.is("#listLayout")) updateLastVisible(layout);
                checkLoadMoreButton(layout);
            }, 600);

            return itemsDisplayed + itemsPerPage;
        }

        function updateLastVisible(layout) {
            layout.find(".loadItem").removeClass("last-visible");
            layout
                .find(".loadItem")
                .not(".hidden")
                .last()
                .addClass("last-visible");
        }

        function checkLoadMoreButton(layout) {
            if (layout.find(".loadItem.hidden").length === 0) {
                if (layout.is("#listLayout")) {
                    $("#loadMoreListBtn").hide();
                    $("#infiniteScrollList").hide();
                } else if (layout.is("#gridLayout")) {
                    $("#loadMoreGridBtn").hide();
                }
            }
        }

        hideExtraItems($("#listLayout"), listItemsDisplayed);
        hideExtraItems($("#gridLayout"), gridItemsDisplayed);

        $("#loadMoreListBtn").on("click", function () {
            listItemsDisplayed = showMoreItems(
                $("#listLayout"),
                listItemsPerPage,
                listItemsDisplayed
            );
        });

        $("#loadMoreGridBtn").on("click", function () {
            gridItemsDisplayed = showMoreItems(
                $("#gridLayout"),
                gridItemsPerPage,
                gridItemsDisplayed
            );
        });
    };

    /* showform
  -------------------------------------------------------------------------------------*/
    var showform = function () {
        if ($(".show-form").length > 0) {
            $(".show-form").on("click", function (e) {
                e.preventDefault();
                $(this).toggleClass("click");
                $(".wd-search-form").toggleClass("show");
                $(".wg-filter").toggleClass("active");
            });
        }
    };

    /* hoverTabs 
  -------------------------------------------------------------------------------------*/
    var hoverTabs = function () {
        if (!$(".tabs-hover-wrap").length) return;
        $(".tabs-hover-wrap").each(function () {
            const $wrapper = $(this);
            const $tabBtns = $wrapper.find(".item");
            const $tabContents = $wrapper.find(".tab-content");
            let hoverTimer;
            $tabBtns
                .on("mouseenter", function () {
                    const $this = $(this);
                    hoverTimer = setTimeout(function () {
                        const tabId = $this.data("tab");
                        if (!$this.hasClass("active")) {
                            $tabBtns.removeClass("active");
                            $this.addClass("active");
                            $tabContents.removeClass("active");
                            $wrapper.find(`#${tabId}`).addClass("active");
                        }
                    }, 100);
                })
                .on("mouseleave", function () {
                    clearTimeout(hoverTimer);
                });
            $tabBtns.first().addClass("active");
            $tabContents.first().addClass("active");
        });
    };

    /* infiniteslide
  -------------------------------------------------------------------------------------*/
    const infiniteslide = () => {
        if ($(".infiniteslide").length > 0) {
            $(".infiniteslide").each(function () {
                var $this = $(this);
                var style = $this.data("style") || "left";
                var clone = $this.data("clone") || 4;
                var speed = $this.data("speed") || 100;
                $this.infiniteslide({
                    speed: speed,
                    direction: style,
                    clone: clone,
                });
            });
        }
    };

    /* infiniteslide
  -------------------------------------------------------------------------------------*/
    const showInput = () => {
        if (!$(".form-account").length) return;
        const $passwordInput = $("#password");
        const $confirmPasswordInput = $("#confirmPassword");
        const $newPassword = $("#newPassword");
        function setupPasswordToggle(toggleBtnId, $input) {
            const $toggleBtn = $("#" + toggleBtnId);
            $toggleBtn.on("click", function () {
                const isPassword = $input.attr("type") === "password";
                $input.attr("type", isPassword ? "text" : "password");
                $toggleBtn.html(
                    isPassword
                        ? '<i class="icon-eye"></i>'
                        : '<i class="icon-eye-slash"></i>'
                );
            });
        }

        setupPasswordToggle("toggle-password", $passwordInput);
        setupPasswordToggle("toggle-confirm-password", $confirmPasswordInput);
        setupPasswordToggle("toggle-new-password", $newPassword);
    };

    /* Wish List 
  ------------------------------------------------------------------------------------- */
    var wishList = function () {
        $(".btn-add-wishlist").on("click", function () {
            $(this).toggleClass("added-wishlist");
        });
        $(".card-house .wishlist").on("click", function () {
            $(this).toggleClass("addwishlist");

            let icon = $(this).find(".icon");
            let tooltip = $(this).find(".tooltip");

            if ($(this).hasClass("addwishlist")) {
                icon.removeClass("icon-Heart").addClass("icon-trash-alt-solid");
                tooltip.text("Remove Wishlist");
            } else {
                icon.removeClass("icon-trash-alt-solid").addClass("icon-Heart");
                tooltip.text("Add to Wishlist");
            }
        });
    };

    /* fillterIso
  -------------------------------------------------------------------------------------*/
    const fillterIso = () => {
        if (!$(".fillters-wrap").length) return;
        var $grid = $(".fillters-wrap").isotope({
            itemSelector: ".item-fillter",
            layoutMode: "fitRows",
        });
        $(".tf-filters button").on("click", function () {
            $(".tf-filters button").removeClass("active");
            $(this).addClass("active");
            var filterValue = $(this).attr("data-filter");
            $grid.isotope({ filter: filterValue });
        });
    };

    /* Tab Slide 
  ------------------------------------------------------------------------------------- */
    var tabSlide = function () {
        if ($(".tab-slide").length > 0) {
            function updateTabSlide() {
                var $activeTab = $(".tab-slide li.active");
                if ($activeTab.length > 0) {
                    var $width = $activeTab.width();
                    var $left = $activeTab.position().left;
                    var sideEffect = $activeTab
                        .parent()
                        .find(".item-slide-effect");
                    $(sideEffect).css({
                        width: $width,
                        transform: "translateX(" + $left + "px)",
                    });
                }
            }
            $(".tab-slide li").on("click", function () {
                var itemTab = $(this).parent().find("li");
                $(itemTab).removeClass("active");
                $(this).addClass("active");

                var $width = $(this).width();
                var $left = $(this).position().left;
                var sideEffect = $(this).parent().find(".item-slide-effect");
                $(sideEffect).css({
                    width: $width,
                    transform: "translateX(" + $left + "px)",
                });
            });

            $(window).on("resize", function () {
                updateTabSlide();
            });

            updateTabSlide();
        }
    };

    /* video
  -------------------------------------------------------------------------------------*/
    var video = function () {
        if ($("div").hasClass("widget-video")) {
            $(".popup-youtube").magnificPopup({
                type: "iframe",
            });
        }
    };

    /* hoverActive 
  -------------------------------------------------------------------------------------*/
    var hoverActive = function () {
        $(".wrap-box-hover-active").each(function (index) {
            var $container = $(this);
            var containerId = `hover-container-${index}`;
            $container.attr("data-hover-id", containerId);
            var $hoverItems = $container.find(".item-hover");
            if (
                $container.find(".item-hover.is-active").length === 0 &&
                $hoverItems.length > 0
            ) {
                $hoverItems.first().addClass("is-active");
            }
            $container.on("mouseenter", ".item-hover", function () {
                var $activeItem = $container.find(".item-hover.is-active");
                if ($activeItem.length > 0 && $activeItem[0] !== this) {
                    $activeItem.removeClass("is-active");
                }
                $(this).addClass("is-active");
            });
        });
    };

    /* oneNavOnePage
  -------------------------------------------------------------------------------------*/
    const oneNavOnePage = () => {
        if (!$(".section-onepage").length) return;

        const $navLinks = $(".nav_link");
        const $sections = $(".section");

        $navLinks.on("click", function (e) {
            e.preventDefault();
            const target = $(this).attr("href");
            $("html, body").animate({ scrollTop: $(target).offset().top }, 0);
        });

        const updateActiveMenu = () => {
            const scrollTop = $(window).scrollTop();
            let current = "";
            $sections.each(function () {
                const $section = $(this);
                const top = $section.offset().top - 200;
                const bottom = top + $section.outerHeight();
                if (scrollTop >= top && scrollTop < bottom)
                    current = $section.attr("id");
            });
            $navLinks
                .removeClass("active")
                .filter(`[href="#${current}"]`)
                .addClass("active");
        };

        $(window).on("scroll", updateActiveMenu);
        updateActiveMenu();
    };

    /* sendmail
  -------------------------------------------------------------------------------------*/
    var sendmail = function () {
        if ($(".sib-form").length > 0) {
            window.REQUIRED_CODE_ERROR_MESSAGE = "Please choose a country code";
            window.LOCALE = "en";
            window.EMAIL_INVALID_MESSAGE = window.SMS_INVALID_MESSAGE =
                "The information provided is invalid. Please review the field format and try again.";

            window.REQUIRED_ERROR_MESSAGE = "This field cannot be left blank. ";

            window.GENERIC_INVALID_MESSAGE =
                "The information provided is invalid. Please review the field format and try again.";
            window.translation = {
                common: {
                    selectedList: "{quantity} list selected",
                    selectedLists: "{quantity} lists selected",
                },
            };
            var AUTOHIDE = Boolean(0);
        }
    };

    /* slideBarPrivacy
  -------------------------------------------------------------------------------------*/
    var slideBarPrivacy = function () {
        if (!$(".highlight-bar").length) return;
        const tocItems = document.querySelectorAll(".nav_link");
        const highlightBar = document.querySelector(".highlight-bar");
        let activeIndex = 0;

        function updateHighlightBar(index) {
            const activeItem = tocItems[index];
            if (!activeItem) return;

            const top = activeItem.offsetTop;
            const height = activeItem.offsetHeight;

            highlightBar.style.top = `${top}px`;
            highlightBar.style.height = `${height}px`;
        }

        updateHighlightBar(activeIndex);

        tocItems.forEach((item, index) => {
            item.addEventListener("click", (e) => {
                e.preventDefault();

                tocItems[activeIndex].classList.remove("active");
                item.classList.add("active");
                activeIndex = index;
                updateHighlightBar(index);

                const targetId = item.getAttribute("data-target");
                const targetSection = document.getElementById(targetId);

                if (targetSection) {
                    targetSection.scrollIntoView({
                        behavior: "smooth",
                        block: "start",
                    });
                }
            });

            item.addEventListener("mouseenter", () => {
                updateHighlightBar(index);
            });
        });

        document
            .querySelector(".privacy-table")
            .addEventListener("mouseleave", () => {
                updateHighlightBar(activeIndex);
            });

        // Cập nhật highlight khi resize
        window.addEventListener("resize", () => {
            updateHighlightBar(activeIndex);
        });

        const sectionMap = Array.from(tocItems).map((item) => {
            const targetId = item.getAttribute("data-target");
            const targetSection = document.getElementById(targetId);
            return { item, targetSection };
        });

        function onScroll() {
            let newIndex = activeIndex;

            for (let i = 0; i < sectionMap.length; i++) {
                const { targetSection } = sectionMap[i];
                const rect = targetSection.getBoundingClientRect();

                if (rect.top <= 100 && rect.bottom >= 100) {
                    newIndex = i;
                    break;
                }
            }

            if (newIndex !== activeIndex) {
                tocItems[activeIndex].classList.remove("active");
                tocItems[newIndex].classList.add("active");
                activeIndex = newIndex;
                updateHighlightBar(activeIndex);
            }
        }

        window.addEventListener("scroll", onScroll);
    };

    /* goTop
  -------------------------------------------------------------------------------------*/
    const goTop = () => {
        if ($("div").hasClass("progress-wrap")) {
            var progressPath = document.querySelector(".progress-wrap path");
            var pathLength = progressPath.getTotalLength();
            progressPath.style.transition =
                progressPath.style.WebkitTransition = "none";
            progressPath.style.strokeDasharray = pathLength + " " + pathLength;
            progressPath.style.strokeDashoffset = pathLength;
            progressPath.getBoundingClientRect();
            progressPath.style.transition =
                progressPath.style.WebkitTransition =
                    "stroke-dashoffset 10ms linear";
            var updateprogress = function () {
                var scroll = $(window).scrollTop();
                var height = $(document).height() - $(window).height();
                var progress = pathLength - (scroll * pathLength) / height;
                progressPath.style.strokeDashoffset = progress;
            };
            updateprogress();
            $(window).scroll(updateprogress);
            var offset = 200;
            var duration = 0;
            jQuery(window).on("scroll", function () {
                if (jQuery(this).scrollTop() > offset) {
                    jQuery(".progress-wrap").addClass("active-progress");
                } else {
                    jQuery(".progress-wrap").removeClass("active-progress");
                }
            });
            jQuery(".progress-wrap").on("click", function (event) {
                event.preventDefault();
                jQuery("html, body").animate({ scrollTop: 0 }, duration);
                return false;
            });
        }
    };

    /* action_click
  -------------------------------------------------------------------------------------*/
    var action_click = function () {
        if ($(".tf-action-btns").length > 0) {
            $(".tf-action-btns").on("click", function () {
                $(this).toggleClass("active");
            });
        }
    };

    /* datePicker
  -------------------------------------------------------------------------------------*/
    var datePicker = function () {
        [
            "#datepicker1",
            "#datepicker2",
            "#datepicker3",
            "#datepicker4",
            "#datepicker5",
            "#datepicker6",
        ].forEach(function (id) {
            if ($(id).length) {
                $(id).datepicker({
                    firstDay: 1,
                    dateFormat: "dd/mm/yy",
                });
            }
        });
    };

    /* Delete image 
  -------------------------------------------------------------------------------------*/
    var deleteImg = function () {
        if ($(".remove-file").length > 0) {
            const swalWithBootstrapButtons = Swal.mixin({
                customClass: {
                    confirmButton: "btn btn-success",
                    cancelButton: "btn btn-danger",
                },
                buttonsStyling: false,
            });

            $(".remove-file").on("click", function (e) {
                e.preventDefault();
                const $this = $(this); // store element to remove later

                swalWithBootstrapButtons
                    .fire({
                        title: "Are you sure you want to delete?",
                        text: "This action cannot be undone!",
                        icon: "warning",
                        showCancelButton: true,
                        confirmButtonText: "Yes, delete it!",
                        cancelButtonText: "Cancel",
                        reverseButtons: true,
                    })
                    .then((result) => {
                        if (result.isConfirmed) {
                            $this.closest(".file-delete").remove();

                            swalWithBootstrapButtons.fire({
                                title: "Deleted!",
                                text: "Your file has been deleted.",
                                icon: "success",
                            });
                        } else if (
                            result.dismiss === Swal.DismissReason.cancel
                        ) {
                            swalWithBootstrapButtons.fire({
                                title: "Cancelled",
                                text: "Your file is safe.",
                                icon: "error",
                            });
                        }
                    });
            });
        }
    };

    /* Handle dashboard
  -------------------------------------------------------------------------------------*/
    var showHideDashboard = function () {
        if ($(".button-show-hide").length > 0) {
            $(".button-show-hide").on("click", function () {
                $(".page-layout").toggleClass("full-width");
            });
            $(".mobile-nav-toggler,.overlay-dashboard").on(
                "click",
                function () {
                    $(".page-layout").removeClass("full-width");
                }
            );
        }
    };

    // Dom Ready
    $(function () {
        preventDefault();
        headerFixed();
        headerFixed2();
        handleFooter();
        effect_button();
        loadProduct();
        showform();
        hoverTabs();
        infiniteslide();
        showInput();
        wishList();
        fillterIso();
        tabSlide();
        video();
        hoverActive();
        oneNavOnePage();
        sendmail();
        slideBarPrivacy();
        goTop();
        action_click();
        datePicker();
        deleteImg();
        showHideDashboard();
    });
})(jQuery);
