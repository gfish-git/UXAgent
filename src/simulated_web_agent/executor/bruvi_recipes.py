# Bruvi.com website navigation and interaction recipes
# Based on the website structure at https://bruvi.com/

# URGENT: AGGRESSIVE POPUP DISMISSAL - MUST BE FIRST ACTION
urgent_popup_dismissal = {
    "selector": "body",
    "name": "page_body",
    "class": "urgent-popup-dismissal",
    "children": [
        # MOST AGGRESSIVE: Target Klaviyo popup specifically
        {
            "selector": "[data-testid='klaviyo-form-WfycUb'], [data-testid*='klaviyo'], .klaviyo-form, form[aria-live='polite']",
            "clickable": True,
            "name": "dismiss_klaviyo_immediately",
            "add_text": True,
            "class": "emergency-action"
        },
        # Emergency close buttons
        {
            "selector": "button[aria-label*='close'], button[aria-label*='Close'], .klaviyo-close-form, .close, .dismiss",
            "clickable": True,
            "name": "emergency_close_button",
            "add_text": True,
            "class": "emergency-action"
        },
        # Click outside popups
        {
            "selector": "body",
            "clickable": True,
            "name": "click_body_to_dismiss",
            "add_text": True,
        },
    ]
}

# CRITICAL: Age check banner - MUST BE HANDLED FIRST on every page
age_check_banner = {
    "selector": "age-check-banner, .age-check-banner",
    "name": "age_verification",
    "children": [
        {
            "selector": "h2, .age-check-banner__heading",
            "add_text": True,
            "name": "age_check_title"
        },
        {
            "selector": "p, .age-check-banner__text",
            "add_text": True,
            "name": "age_check_description"
        },
        # The "Yes, I'm 21 or older" button - HIGHEST PRIORITY
        {
            "selector": "button[data-age-check='true'], .age-check-banner__button--primary, button:contains('21 or older')",
            "clickable": True,
            "name": "confirm_age_21",
            "add_text": True,
            "class": "critical-action"
        },
        # Fallback age confirmation
        {
            "selector": "button, .age-check-banner__button",
            "clickable": True,
            "name": "age_check_button",
            "add_text": True,
        }
    ]
}

# Enhanced navigation structure with direct URL targeting
nav = {
    "selector": "header, nav, .header__inline-menu, sticky-header",
    "children": [
        # DIRECT URL NAVIGATION - HIGHEST PRIORITY to bypass all popups
        {
            "selector": "a[href='/collections/brewers']",
            "clickable": True,
            "name": "direct_brewers_link",
            "add_text": True,
            "class": "emergency-action"
        },
        {
            "selector": "a[href='/pages/build-your-own-bundle']",
            "clickable": True,
            "name": "direct_bundle_builder_link",
            "add_text": True,
            "class": "emergency-action"
        },
        {
            "selector": "a[href='/pages/brewer-subscription-bundle']",
            "clickable": True,
            "name": "direct_bundle_landing_link",
            "add_text": True,
            "class": "emergency-action"
        },
        # Header navigation fallbacks
        {
            "selector": "#HeaderMenu-brewers, a[href*='/collections/brewers']",
            "clickable": True,
            "name": "header_brewers_link",
            "add_text": True,
            "class": "critical-action"
        },
        {
            "selector": "#HeaderMenu-bundles, a[href*='/collections/bundles']",
            "clickable": True,
            "name": "header_bundles_link", 
            "add_text": True,
            "class": "critical-action"
        },
    ]
}

# Main recipes array following the correct format
recipes = [
    # Homepage recipe with AGGRESSIVE POPUP DISMISSAL FIRST
    {
        "match": "/",
        "match_method": "url",
        "selector": "html",
        "children": [
            {"selector": "head", "children": [{"selector": "title", "add_text": True}]},
            {
                "selector": "body",
                "children": [
                    # EMERGENCY: DISMISS ALL POPUPS IMMEDIATELY
                    urgent_popup_dismissal,
                    # Handle age check
                    age_check_banner,
                    # DIRECT NAVIGATION - Skip problematic main content entirely
                    nav,
                    # Main content with GUARANTEED clickable elements
                    {
                        "selector": "main, .main-content, .content-for-layout",
                        "children": [
                            {
                                "selector": "h1, h2, .banner__heading",
                                "add_text": True,
                                "class": "page-title",
                            },
                            {
                                "selector": "p, .banner__text",
                                "add_text": True,
                            },
                            # GUARANTEED clickable links - these should always exist
                            {
                                "selector": "a[href*='build-your-own-bundle']",
                                "clickable": True,
                                "name": "bundle_builder_direct_link",
                                "add_text": True,
                                "class": "priority-action"
                            },
                            {
                                "selector": "a[href*='/collections/brewers']",
                                "clickable": True,
                                "name": "brewers_direct_link",
                                "add_text": True,
                                "class": "priority-action"
                            },
                            {
                                "selector": "a[href*='brewer'], a[href*='bundle'], a[href*='subscription']",
                                "clickable": True,
                                "name": "coffee_related_link",
                                "add_text": True,
                                "class": "priority-action"
                            },
                            # FALLBACK: Any button or link on the page
                            {
                                "selector": "a, button, .btn, .button",
                                "clickable": True,
                                "name": "any_clickable_element",
                                "add_text": True,
                            },
                        ],
                    },
                ],
            },
        ],
    },
    
    # BUNDLE LANDING PAGE 
    {
        "match": "/pages/brewer-subscription-bundle",
        "match_method": "url",
        "selector": "html",
        "children": [
            {"selector": "head", "children": [{"selector": "title", "add_text": True}]},
            {
                "selector": "body",
                "children": [
                    urgent_popup_dismissal,
                    age_check_banner,
                    nav,
                    {
                        "selector": "main, .content-for-layout, #MainContent",
                        "name": "bundle_landing_page",
                        "children": [
                            {
                                "selector": "h1, h2, .banner__heading",
                                "add_text": True,
                                "class": "page-title",
                            },
                            # THE KEY BUTTON - "Get Started Now" to proceed to bundle builder
                            {
                                "selector": "a[href*='build-your-own-bundle']",
                                "clickable": True,
                                "name": "get_started_bundle",
                                "add_text": True,
                                "class": "critical-action"
                            },
                            # FALLBACK: Any button that might start the bundle process
                            {
                                "selector": "a, button, .btn, .button",
                                "clickable": True,
                                "name": "bundle_landing_action",
                                "add_text": True,
                            },
                        ],
                    },
                ],
            },
        ],
    },

    # ACTUAL BUNDLE BUILDER PAGE - with SPECIFIC button differentiation
    {
        "match": "/pages/build-your-own-bundle",
        "match_method": "url",
        "selector": "html",
        "children": [
            {"selector": "head", "children": [{"selector": "title", "add_text": True}]},
            {
                "selector": "body",
                "children": [
                    urgent_popup_dismissal,
                    age_check_banner,
                    nav,
                    {
                        "selector": "main, .main-content, .bundle-builder, .subscription-builder",
                        "name": "bundle_builder",
                        "children": [
                            {
                                "selector": "h1, .page-title, .bundle-title",
                                "add_text": True,
                                "class": "page-title",
                            },
                            # Bundle building with VERY specific button names to avoid loops
                            {
                                "selector": "form, .bundle-form, .subscription-form",
                                "name": "bundle_builder_form",
                                "children": [
                                    # COFFEE TYPE SELECTION - First step
                                    {
                                        "selector": ".coffee-section, .type-section, .category-section",
                                        "name": "coffee_type_selection",
                                        "children": [
                                            {
                                                "selector": "button:contains('Coffee'):not([disabled]), input[value*='Coffee']:not([disabled])",
                                                "clickable": True,
                                                "name": "select_coffee_type",
                                                "add_text": True,
                                                "class": "critical-action",
                                            },
                                            {
                                                "selector": "button:contains('Espresso'):not([disabled]), input[value*='Espresso']:not([disabled])",
                                                "clickable": True,
                                                "name": "select_espresso_type",
                                                "add_text": True,
                                                "class": "critical-action",
                                            },
                                            {
                                                "selector": "button:contains('Variety'):not([disabled]), input[value*='Variety']:not([disabled])",
                                                "clickable": True,
                                                "name": "select_variety_type",
                                                "add_text": True,
                                                "class": "critical-action",
                                            },
                                        ],
                                    },
                                    # QUANTITY CONTROLS - Avoid generic buttons
                                    {
                                        "selector": ".quantity-section, .delivery-section",
                                        "name": "quantity_controls",
                                        "children": [
                                            {
                                                "selector": "button[class*='plus']:not([disabled]), .quantity-plus:not([disabled]), button:contains('+'):not([disabled])",
                                                "clickable": True,
                                                "name": "increase_pod_quantity",
                                                "add_text": True,
                                                "class": "priority-action",
                                            },
                                            {
                                                "selector": "button[class*='minus']:not([disabled]), .quantity-minus:not([disabled]), button:contains('-'):not([disabled])",
                                                "clickable": True,
                                                "name": "decrease_pod_quantity",
                                                "add_text": True,
                                            },
                                        ],
                                    },
                                    # FINAL COMPLETION BUTTONS - Very specific names
                                    {
                                        "selector": "button[class*='complete']:not([disabled]), button[class*='add-to-cart']:not([disabled]), .complete-bundle-btn:not([disabled])",
                                        "clickable": True,
                                        "name": "complete_bundle_purchase",
                                        "add_text": True,
                                        "class": "critical-action",
                                    },
                                    {
                                        "selector": "button[class*='next']:not([disabled]), button[class*='continue']:not([disabled]), .next-step-btn:not([disabled])",
                                        "clickable": True,
                                        "name": "proceed_to_next_step",
                                        "add_text": True,
                                        "class": "priority-action",
                                    },
                                    # BROAD FALLBACK: Any clickable element in the form
                                    {
                                        "selector": "button:not([disabled]), input[type='submit'], input[type='button'], a",
                                        "clickable": True,
                                        "name": "bundle_form_action",
                                        "add_text": True,
                                    },
                                ],
                            },
                            # OUTSIDE FORM: Any other clickable elements
                            {
                                "selector": "a, button, .btn, .button",
                                "clickable": True,
                                "name": "bundle_page_action",
                                "add_text": True,
                            },
                        ],
                    },
                ],
            },
        ],
    },

    # BREWERS collection page
    {
        "match": "/collections/brewers",
        "match_method": "url",
        "selector": "html",
        "children": [
            {"selector": "head", "children": [{"selector": "title", "add_text": True}]},
            {
                "selector": "body",
                "children": [
                    urgent_popup_dismissal,
                    age_check_banner,
                    nav,
                    {
                        "selector": "main, .main-content",
                        "children": [
                            {
                                "selector": "h1, .collection-title",
                                "add_text": True,
                                "class": "page-title",
                            },
                            {
                                "selector": ".product-card, .product-item, .grid-product",
                                "clickable": True,
                                "name": "brewer_product",
                                "add_text": True,
                            },
                            # FALLBACK: Any clickable element on brewers page
                            {
                                "selector": "a, button, .btn, .button",
                                "clickable": True,
                                "name": "brewers_page_action",
                                "add_text": True,
                            },
                        ],
                    },
                ],
            },
        ],
    },

    # Generic fallback for any other Bruvi pages
    {
        "match": ".*",
        "match_method": "regex",
        "selector": "html",
        "children": [
            {"selector": "head", "children": [{"selector": "title", "add_text": True}]},
            {
                "selector": "body",
                "children": [
                    urgent_popup_dismissal,
                    age_check_banner,
                    nav,
                    {
                        "selector": "main, .main-content, .content-for-layout",
                        "children": [
                            {
                                "selector": "h1, h2, .page-title",
                                "add_text": True,
                                "class": "page-title",
                            },
                            # GUARANTEED: There should always be clickable elements
                            {
                                "selector": "a, button, .btn, .button, input[type='submit'], input[type='button']",
                                "clickable": True,
                                "name": "page_action",
                                "add_text": True,
                            },
                        ],
                    },
                ],
            },
        ],
    },
] 