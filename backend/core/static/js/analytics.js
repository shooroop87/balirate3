/**
 * BlisterPerPost Analytics - GA4 Funnel Tracking
 * Воронка: Главная → Регистрация → Онбординг → Оплата → Подписка
 */

window.BPPAnalytics = {
    
    // ===========================================
    // CORE: Отправка событий в GA4 + Yandex
    // ===========================================
    track: function(eventName, params = {}) {
        // Google Analytics 4
        if (typeof gtag !== 'undefined') {
            gtag('event', eventName, params);
            console.log('📊 GA4:', eventName, params);
        }
        
        // Yandex Metrika
        if (typeof ym !== 'undefined') {
            ym(105948994, 'reachGoal', eventName, params);
            console.log('📊 YM:', eventName, params);
        }
    },

    // ===========================================
    // FUNNEL STEP 1: Главная страница
    // ===========================================
    trackHomepageView: function() {
        this.track('homepage_view', {
            page_title: document.title,
            page_location: window.location.href
        });
    },

    // ===========================================
    // FUNNEL STEP 2: Начало регистрации
    // ===========================================
    trackRegistrationStart: function(method = 'email') {
        this.track('registration_start', {
            method: method,  // 'email' или 'google'
            funnel_step: 2
        });
    },

    // ===========================================
    // FUNNEL STEP 3: Регистрация завершена
    // ===========================================
    trackRegistrationComplete: function(method = 'email') {
        this.track('sign_up', {  // стандартное событие GA4
            method: method
        });
        this.track('registration_complete', {
            method: method,
            funnel_step: 3
        });
    },

    // ===========================================
    // FUNNEL STEP 4: Онбординг - Адрес
    // ===========================================
    trackOnboardingAddress: function() {
        this.track('onboarding_address', {
            funnel_step: 4,
            step_name: 'address'
        });
    },

    trackOnboardingAddressComplete: function() {
        this.track('onboarding_address_complete', {
            funnel_step: 4,
            step_name: 'address'
        });
    },

    // ===========================================
    // FUNNEL STEP 5: Онбординг - Документы
    // ===========================================
    trackOnboardingDocuments: function() {
        this.track('onboarding_documents', {
            funnel_step: 5,
            step_name: 'documents'
        });
    },

    trackDocumentUpload: function(docType) {
        this.track('document_upload', {
            document_type: docType,  // 'e_rezept', 'paper_rezept', 'insurance'
            funnel_step: 5
        });
    },

    trackOnboardingDocumentsComplete: function() {
        this.track('onboarding_documents_complete', {
            funnel_step: 5,
            step_name: 'documents'
        });
    },

    // ===========================================
    // FUNNEL STEP 6: Онбординг - Выбор плана
    // ===========================================
    trackOnboardingPlan: function() {
        this.track('onboarding_plan', {
            funnel_step: 6,
            step_name: 'plan_selection'
        });
    },

    trackPlanSelected: function(planName, planPrice, planInterval) {
        this.track('select_item', {  // стандартное событие GA4
            item_name: planName,
            price: planPrice,
            currency: 'EUR'
        });
        this.track('plan_selected', {
            plan_name: planName,
            plan_price: planPrice,
            plan_interval: planInterval,  // 'weekly', 'monthly', 'quarterly'
            funnel_step: 6
        });
    },

    // ===========================================
    // FUNNEL STEP 7: Начало оплаты
    // ===========================================
    trackPaymentInitiated: function(planName, planPrice) {
        this.track('begin_checkout', {  // стандартное событие GA4
            currency: 'EUR',
            value: planPrice,
            items: [{
                item_name: planName,
                price: planPrice
            }]
        });
        this.track('payment_initiated', {
            plan_name: planName,
            plan_price: planPrice,
            funnel_step: 7
        });
    },

    // ===========================================
    // FUNNEL STEP 8: Подписка оформлена
    // ===========================================
    trackSubscriptionComplete: function(planName, planPrice, subscriptionId) {
        this.track('purchase', {  // стандартное событие GA4
            currency: 'EUR',
            value: planPrice,
            transaction_id: subscriptionId,
            items: [{
                item_name: planName,
                price: planPrice
            }]
        });
        this.track('subscription_complete', {
            plan_name: planName,
            plan_price: planPrice,
            subscription_id: subscriptionId,
            funnel_step: 8
        });
    },

    // ===========================================
    // ДОПОЛНИТЕЛЬНО: Клики CTA
    // ===========================================
    trackCTAClick: function(ctaName, ctaLocation) {
        this.track('cta_click', {
            cta_name: ctaName,
            cta_location: ctaLocation  // 'hero', 'pricing', 'footer'
        });
    },

    // ===========================================
    // ДОПОЛНИТЕЛЬНО: FAQ
    // ===========================================
    trackFAQOpen: function(question) {
        this.track('faq_open', {
            question: question
        });
    },

    // ===========================================
    // ДОПОЛНИТЕЛЬНО: Ошибки
    // ===========================================
    trackError: function(errorType, errorMessage, funnelStep) {
        this.track('form_error', {
            error_type: errorType,
            error_message: errorMessage,
            funnel_step: funnelStep
        });
    }
};

// Auto-init на главной
document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname === '/') {
        BPPAnalytics.trackHomepageView();
    }
});