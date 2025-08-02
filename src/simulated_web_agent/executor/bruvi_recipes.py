# Bruvi.com website navigation and interaction recipes
# Based on the website structure at https://bruvi.com/

# Main navigation structure for Bruvi homepage
nav = {
    "selector": "header, nav",
    "children": [
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
            "selector": "a[href*='brewers']",
            "clickable": True,
            "name": "brewers_nav",
            "add_text": True,
        },
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
] 