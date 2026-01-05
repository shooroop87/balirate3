// backend/core/static/tinymce/plugins/swipergallery/plugin.js
(function() {
    'use strict';
    
    tinymce.PluginManager.add('swipergallery', function(editor, url) {
        // Регистрация кнопки
        editor.ui.registry.addButton('swipergallery', {
            text: 'Gallery',
            tooltip: 'Insert Swiper Gallery',
            icon: 'gallery',
            onAction: function() {
                editor.windowManager.open({
                    title: 'Insert Swiper Gallery',
                    body: {
                        type: 'panel',
                        items: [{
                            type: 'textarea',
                            name: 'images',
                            label: 'Image URLs (one per line)',
                            multiline: true,
                            minHeight: 200
                        }]
                    },
                    buttons: [
                        { type: 'cancel', text: 'Cancel' },
                        { type: 'submit', text: 'Insert', primary: true }
                    ],
                    onSubmit: function(api) {
                        var data = api.getData();
                        var urls = data.images.split('\n').filter(function(url) {
                            return url.trim() !== '';
                        });
                        
                        if (urls.length === 0) {
                            editor.notificationManager.open({
                                text: 'Please enter at least one image URL',
                                type: 'error'
                            });
                            return;
                        }
                        
                        // Генерируем уникальный ID для галереи
                        var galleryId = 'swiper-gallery-' + Date.now();
                        
                        var html = '<div class="swiper ' + galleryId + '" style="width:100%;max-width:800px;margin:20px auto;">';
                        html += '<div class="swiper-wrapper">';
                        urls.forEach(function(url) {
                            html += '<div class="swiper-slide"><img src="' + url.trim() + '" alt="Gallery image" style="width:100%;height:auto;display:block;"></div>';
                        });
                        html += '</div>';
                        html += '<div class="swiper-pagination"></div>';
                        html += '<div class="swiper-button-prev"></div>';
                        html += '<div class="swiper-button-next"></div>';
                        html += '</div>';
                        
                        // Скрипт для инициализации Swiper
                        html += '<script>';
                        html += '(function() {';
                        html += '  if (typeof Swiper !== "undefined") {';
                        html += '    new Swiper(".' + galleryId + '", {';
                        html += '      loop: true,';
                        html += '      pagination: { el: ".' + galleryId + ' .swiper-pagination", clickable: true },';
                        html += '      navigation: { nextEl: ".' + galleryId + ' .swiper-button-next", prevEl: ".' + galleryId + ' .swiper-button-prev" }';
                        html += '    });';
                        html += '  }';
                        html += '})();';
                        html += '</script>';
                        
                        editor.insertContent(html);
                        api.close();
                    }
                });
            }
        });
        
        return {
            getMetadata: function() {
                return {
                    name: 'Swiper Gallery Plugin',
                    url: 'https://swiperjs.com'
                };
            }
        };
    });
})();