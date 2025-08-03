# Bruvi.com website navigation and interaction recipes
# Based on the website structure at https://bruvi.com/

# CRITICAL: Popup dismissal for Klaviyo email signup forms - MUST BE HANDLED FIRST
popup_dismissal = {
    "selector": "[data-testid*='klaviyo'], .klaviyo-form, .popup, .modal, .overlay, .newsletter-popup, form[aria-live='polite']",
    "name": "popup_container",
    "children": [
        # Close button - try multiple common patterns
        {
            "selector": "button[aria-label*='close'], button[aria-label*='Close'], .close, .dismiss, [data-testid*='close'], .klaviyo-close-form, button[class*='close'], button[type='button']",
            "clickable": True,
            "name": "close_popup",
            "add_text": True,
            "class": "priority-action"
        },
        # Sometimes clicking the form background dismisses it
        {
            "selector": ".klaviyo-form, [data-testid*='klaviyo-form']",
            "clickable": True,
            "name": "dismiss_form",
            "add_text": True,
        },
        # Overlay background
        {
            "selector": ".overlay-background, .modal-background, .backdrop",
            "clickable": True,
            "name": "dismiss_overlay",
        },
        # Try clicking outside the form
        {
            "selector": "body",
            "clickable": True,
            "name": "click_outside",
        },
    ]
}

# Main navigation structure for Bruvi homepage
nav = {
    "selector": "header, nav",
    "children": [
        # BREWERS navigation - prioritize this for coffee machines
        {
            "selector": "a[href*='brewers'], a[href*='brewer'], nav a[href*='brewers']",
            "clickable": True,
            "name": "brewers_button",
            "add_text": True,
            "class": "primary-nav-link"
        },
        {
            "selector": "input[type='search'], .search-input, input[placeholder*='search']",  
            "name": "search_input",
        },
        {
            "selector": "button[type='submit'], .search-button",
            "clickable": True,
            "name": "search_button",
        },
        # Main navigation links
        {
            "selector": "a[href*='pods']",
            "clickable": True, 
            "name": "pods_nav",
            "add_text": True,
        },
        {
            "selector": "a[href*='cart'], .cart-icon",
            "clickable": True,
            "name": "cart_nav",
            "add_text": True,
        },
    ],
}

# Product cards for coffee machines/brewers
product_card = {
    "selector": ".product-card, .brewer-card, .coffee-machine",
    "name": "from_text",
    "text_selector": "h2, h3, .product-title, .brewer-title",
    "clickable": True,
    "children": [
        {
            "selector": "img",
            "keep_attr": {"src": True, "alt": True},
        },
        {
            "selector": "h2, h3, .product-title, .brewer-title",
            "add_text": True,
            "class": "product-name",
        },
        {
            "selector": ".price, .product-price, [class*='price']",
            "add_text": True,
            "class": "product-price",
        },
        {
            "selector": ".rating, .stars, [class*='rating']",
            "add_text": True,
            "class": "product-rating",
        },
        {
            "selector": "button[class*='add'], .add-to-cart",
            "clickable": True,
            "name": "add_to_cart",
            "add_text": True,
        },
        {
            "selector": "a[href*='view'], a[href*='details'], .view-product",
            "clickable": True,
            "name": "view_product",
            "add_text": True,
        },
    ],
}

# Coffee machine categories
category_section = {
    "selector": ".category-section, .coffee-types, .brew-options",
    "children": [
        {
            "selector": "h2, h3, .category-title",
            "add_text": True,
            "class": "category-title",
        },
        {
            "selector": ".category-item, .coffee-type, .brew-option",
            "name": "from_text", 
            "text_selector": "h3, h4, .item-title",
            "clickable": True,
            "children": [
                {
                    "selector": "img",
                    "keep_attr": {"src": True, "alt": True},
                },
                {
                    "selector": "h3, h4, .item-title",
                    "add_text": True,
                },
                {
                    "selector": "p, .description",
                    "add_text": True,
                    "class": "item-description",
                },
            ],
        },
    ],
}

recipes = [
    # Homepage recipe
    {
        "match": "/",
        "match_method": "url",
        "selector": "html",
        "children": [
            {"selector": "head", "children": [{"selector": "title", "add_text": True}]},
            {
                "selector": "body",
                "children": [
                    # CRITICAL: Handle popups FIRST before any navigation
                    popup_dismissal,
                    nav,
                    # Hero section with main CTA
                    {
                        "selector": ".hero, .main-banner, [class*='hero']",
                        "children": [
                            {
                                "selector": "h1, .hero-title, .main-title",
                                "add_text": True,
                                "class": "hero-title",
                            },
                            {
                                "selector": "button[class*='shop'], button[class*='get'], .cta-button",
                                "clickable": True,
                                "name": "main_cta",
                                "add_text": True,
                            },
                        ],
                    },
                    # Product categories section
                    {
                        "selector": ".product-categories, .shop-section",
                        "name": "product_categories",
                        "children": [category_section],
                    },
                    # Coffee machine features
                    {
                        "selector": ".features, .benefits, .why-bruvi",
                        "children": [
                            {
                                "selector": ".feature-item, .benefit-item",
                                "name": "from_text",
                                "text_selector": "h3, h4, .feature-title",
                                "children": [
                                    {
                                        "selector": "h3, h4, .feature-title",
                                        "add_text": True,
                                    },
                                    {
                                        "selector": "p, .feature-description",
                                        "add_text": True,
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        ],
    },
    # Brewers/coffee machines page
    {
        "match": "/brewers",
        "match_method": "url",
        "selector": "html", 
        "children": [
            {"selector": "head", "children": [{"selector": "title", "add_text": True}]},
            {
                "selector": "body",
                "children": [
                    nav,
                    # Main content area
                    {
                        "selector": "main, .main-content, .brewers-page",
                        "children": [
                            {
                                "selector": "h1, .page-title",
                                "add_text": True,
                                "class": "page-title",
                            },
                            # Coffee machine products
                            {
                                "selector": ".products, .brewers-grid, .coffee-machines",
                                "name": "coffee_machines",
                                "children": [product_card],
                            },
                            # Filters/refinements
                            {
                                "selector": ".filters, .refinements, .sort-options",
                                "name": "filters",
                                "children": [
                                    {
                                        "selector": ".filter-item, .sort-option",
                                        "name": "from_text",
                                        "text_selector": "label, .filter-label",
                                        "clickable": True,
                                        "children": [
                                            {
                                                "selector": "input[type='checkbox'], input[type='radio']",
                                                "name": "filter_checkbox",
                                            },
                                            {
                                                "selector": "label, .filter-label",
                                                "add_text": True,
                                            },
                                        ],
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        ],
    },
    # Product details page
    {
        "match": "/products/",
        "match_method": "url",
        "selector": "html",
        "children": [
            {"selector": "head", "children": [{"selector": "title", "add_text": True}]},
            {
                "selector": "body", 
                "children": [
                    nav,
                    # Product details
                    {
                        "selector": "main, .product-details, .coffee-machine-details",
                        "children": [
                            {
                                "selector": ".product-info, .coffee-machine-info",
                                "children": [
                                    {
                                        "selector": "h1, .product-title",
                                        "add_text": True,
                                        "class": "product-title",
                                    },
                                    {
                                        "selector": ".price, .product-price",
                                        "add_text": True,
                                        "class": "product-price",
                                    },
                                    {
                                        "selector": ".rating, .reviews",
                                        "add_text": True,
                                        "class": "product-rating",
                                    },
                                    {
                                        "selector": ".description, .product-description",
                                        "add_text": True,
                                        "class": "product-description",
                                    },
                                ],
                            },
                            # Add to cart section
                            {
                                "selector": ".add-to-cart-section, .purchase-options",
                                "name": "purchase_section",
                                "children": [
                                    {
                                        "selector": "button[class*='cart'], .add-to-cart-btn",
                                        "clickable": True,
                                        "name": "add_to_cart",
                                        "add_text": True,
                                        "class": "add-to-cart-button",
                                    },
                                    {
                                        "selector": "button[class*='buy'], .buy-now-btn",
                                        "clickable": True,
                                        "name": "buy_now",
                                        "add_text": True,
                                        "class": "buy-now-button",
                                    },
                                    # Product options/variants
                                    {
                                        "selector": ".product-options, .variants",
                                        "children": [
                                            {
                                                "selector": "select, .option-select",
                                                "name": "from_text",
                                                "text_selector": "option[selected], .selected-option",
                                                "children": [
                                                    {
                                                        "selector": "option",
                                                        "name": "from_text",
                                                        "text_selector": "self",
                                                        "clickable": True,
                                                        "add_text": True,
                                                    },
                                                ],
                                            },
                                        ],
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        ],
    },
    # Cart page
    {
        "match": "/cart",
        "match_method": "url", 
        "selector": "html",
        "children": [
            {"selector": "head", "children": [{"selector": "title", "add_text": True}]},
            {
                "selector": "body",
                "children": [
                    nav,
                    {
                        "selector": "main, .cart-page",
                        "children": [
                            {
                                "selector": "h1, .cart-title",
                                "add_text": True,
                                "class": "page-title",
                            },
                            # Cart items
                            {
                                "selector": ".cart-items, .cart-products",
                                "children": [
                                    {
                                        "selector": ".cart-item, .cart-product",
                                        "name": "from_text",
                                        "text_selector": ".item-name, .product-name",
                                        "children": [
                                            {
                                                "selector": ".item-name, .product-name",
                                                "add_text": True,
                                            },
                                            {
                                                "selector": ".item-price, .product-price",
                                                "add_text": True,
                                            },
                                            {
                                                "selector": ".quantity-input, input[type='number']",
                                                "name": "quantity",
                                            },
                                            {
                                                "selector": "button[class*='remove'], .remove-btn",
                                                "clickable": True,
                                                "name": "remove_item",
                                                "add_text": True,
                                            },
                                        ],
                                    },
                                ],
                            },
                            # Checkout section
                            {
                                "selector": ".checkout-section, .cart-summary",
                                "children": [
                                    {
                                        "selector": ".total, .cart-total",
                                        "add_text": True,
                                        "class": "cart-total",
                                    },
                                    {
                                        "selector": "button[class*='checkout'], .checkout-btn",
                                        "clickable": True,
                                        "name": "checkout",
                                        "add_text": True,
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        ],
    },
    # Build Your Own Bundle page - where users customize their subscription
    {
        "match": "/pages/build-your-own-bundle",
        "match_method": "url", 
        "selector": "html",
        "children": [
            {"selector": "head", "children": [{"selector": "title", "add_text": True}]},
            {
                "selector": "body",
                "children": [
                    # Handle any remaining popups first
                    popup_dismissal,
                    # Navigation should still be available
                    nav,
                    # Main bundle builder content
                    {
                        "selector": "main, .main-content, .bundle-builder, .subscription-builder, .page-content, .container",
                        "children": [
                            {
                                "selector": "h1, .page-title, .bundle-title",
                                "add_text": True,
                                "class": "page-title",
                            },
                            # Primary bundle building interface - make this the highest priority
                            {
                                "selector": ".bundle-form, .subscription-form, form, .build-bundle, .bundle-container",
                                "name": "bundle_builder",
                                "children": [
                                    # Step 1: Coffee machine/brewer selection - MOST IMPORTANT for Jessica
                                    {
                                        "selector": ".brewer-section, .machine-section, .step-1, .brewer-options, [data-step='1'], .product-selection",
                                        "name": "brewer_selection",
                                        "children": [
                                            {
                                                "selector": "h2, h3, .step-title, .section-title",
                                                "add_text": True,
                                            },
                                            # Individual brewer/machine options
                                            {
                                                "selector": ".brewer-option, .machine-option, .product-card, .brewer-card, .coffee-machine",
                                                "clickable": True,
                                                "name": "choose_brewer",
                                                "add_text": True,
                                                "children": [
                                                    {
                                                        "selector": "h4, h5, .brewer-name, .product-name, .machine-title",
                                                        "add_text": True,
                                                    },
                                                    {
                                                        "selector": ".price, .brewer-price, .product-price",
                                                        "add_text": True,
                                                    },
                                                    {
                                                        "selector": ".description, .brewer-description, .features",
                                                        "add_text": True,
                                                    },
                                                    {
                                                        "selector": "button, .select-btn, .choose-btn, input[type='radio']",
                                                        "clickable": True,
                                                        "name": "select_this_brewer",
                                                        "add_text": True,
                                                    },
                                                ],
                                            },
                                        ],
                                    },
                                    # Step 2: Subscription pod selection
                                    {
                                        "selector": ".pods-section, .subscription-section, .step-2, .pod-options, [data-step='2']",
                                        "name": "pod_selection",
                                        "children": [
                                            {
                                                "selector": "h2, h3, .step-title, .section-title",
                                                "add_text": True,
                                            },
                                            # Pod variety selection
                                            {
                                                "selector": ".pod-option, .pod-variety, .coffee-type",
                                                "clickable": True,
                                                "name": "choose_pods",
                                                "add_text": True,
                                                "children": [
                                                    {
                                                        "selector": "h4, h5, .pod-name, .coffee-name",
                                                        "add_text": True,
                                                    },
                                                    {
                                                        "selector": ".pod-description, .coffee-description",
                                                        "add_text": True,
                                                    },
                                                    {
                                                        "selector": "button, .add-pod-btn, input[type='checkbox']",
                                                        "clickable": True,
                                                        "name": "add_pod_type",
                                                        "add_text": True,
                                                    },
                                                ],
                                            },
                                        ],
                                    },
                                    # Step 3: Delivery frequency and quantity
                                    {
                                        "selector": ".frequency-section, .delivery-section, .step-3, [data-step='3']",
                                        "name": "delivery_options",
                                        "children": [
                                            {
                                                "selector": "h2, h3, .step-title, .section-title",
                                                "add_text": True,
                                            },
                                            # Frequency options (weekly, monthly, etc.)
                                            {
                                                "selector": ".frequency-option, .delivery-frequency",
                                                "clickable": True,
                                                "name": "choose_frequency",
                                                "add_text": True,
                                                "children": [
                                                    {
                                                        "selector": "button, input[type='radio'], .frequency-btn",
                                                        "clickable": True,
                                                        "name": "select_frequency",
                                                        "add_text": True,
                                                    },
                                                ],
                                            },
                                            # Quantity selector
                                            {
                                                "selector": ".quantity-section, .pod-quantity",
                                                "children": [
                                                    {
                                                        "selector": "input[type='number'], select, .quantity-input",
                                                        "name": "pod_quantity",
                                                    },
                                                    {
                                                        "selector": "button.plus, button.minus, .quantity-btn",
                                                        "clickable": True,
                                                        "name": "adjust_quantity",
                                                        "add_text": True,
                                                    },
                                                ],
                                            },
                                        ],
                                    },
                                    # Final step: Bundle summary and add to cart
                                    {
                                        "selector": ".bundle-summary, .cart-section, .final-step, .checkout-section",
                                        "name": "bundle_summary",
                                        "children": [
                                            {
                                                "selector": "h2, h3, .summary-title",
                                                "add_text": True,
                                            },
                                            {
                                                "selector": ".total-price, .bundle-total, .final-price",
                                                "add_text": True,
                                                "class": "bundle-total",
                                            },
                                            {
                                                "selector": ".selected-items, .bundle-contents",
                                                "add_text": True,
                                            },
                                            # The key action button for Jessica
                                            {
                                                "selector": "button[class*='cart'], button[class*='add'], .add-to-cart-btn, .add-bundle-btn, .complete-bundle-btn",
                                                "clickable": True,
                                                "name": "complete_bundle_purchase",
                                                "add_text": True,
                                                "class": "primary-action",
                                            },
                                        ],
                                    },
                                ],
                            },
                            # Fallback selectors for any other bundle elements
                            {
                                "selector": "section, .section, div[class*='bundle'], div[class*='subscription']",
                                "children": [
                                    {
                                        "selector": "button, .btn, input[type='submit'], input[type='button']",
                                        "clickable": True,
                                        "name": "bundle_action_button",
                                        "add_text": True,
                                    },
                                    {
                                        "selector": ".card, .option, .choice, .selection",
                                        "clickable": True,
                                        "name": "bundle_option",
                                        "add_text": True,
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        ],
    },
] 