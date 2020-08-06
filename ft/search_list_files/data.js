ftSuiteConfig.dataSource = {
    "total": 6,
    "pageItems": [

    {

        "id": "article1",
        "title": {
            "title": "Business turns to nature to fight climate change"
        },

        "location": {
            "uri": "https://www.ft.com/content/7d940587-4502-4468-acea-a67b7bf6a523"
        },
        "images": [{
            "url": "https://www.ft.com/__origami/service/image/v2/images/raw/https%3A%2F%2Fd1e00ek4ebabms.cloudfront.net%2Fproduction%2F0c1eb134-2f52-4f9e-8ffc-b2611e13147e.jpg?source=next&fit=scale-down&dpr=2&width=340",
            "type": "primary",
            "mediaType": "image/jpeg"
        }],

    },

    {
        "id": "article2",
        "title": {
            "title": "Why we need to declare a global climate emergency now"
        },

        "location": {
            "uri": "https://www.ft.com/content/b4a112dd-cafd-4522-bf79-9e25704577ab"
        },
        "images": [{
            "url": "https://www.ft.com/__origami/service/image/v2/images/raw/https%3A%2F%2Fd1e00ek4ebabms.cloudfront.net%2Fproduction%2F56da7e1f-dab0-4380-be3c-a799b381a74e.jpg?source=next&fit=scale-down&dpr=2&width=340",
            "type": "primary",
            "mediaType": "image/jpeg"
        }],
    },

    {
        "id": "article3",
        "title": {
            "title": "P&G urged to match best in class to avoid ‘greenwash’ label"
        },
        "location": {
            "uri": "https://www.ft.com/content/4f807d17-2f95-4572-a7f4-50655fdda00e"
        },
        "images": [{
            "url": "https://www.ft.com/__origami/service/image/v2/images/raw/https%3A%2F%2Fd1e00ek4ebabms.cloudfront.net%2Fproduction%2F009adadd-428c-487e-b6e4-7b52dd803b95.jpg?source=next&fit=scale-down&dpr=2&width=340",
            "type": "primary",
            "mediaType": "image/jpeg"
        }],
    },

    {
        "id": "article4",
        "title": {
            "title": "ESG investors wake up to biodiversity risk"
        },
        "location": {
            "uri": "https://www.ft.com/content/100f0c5b-83c5-4e9a-8ad0-89af2ea4a758"
        },
        "images": [{
            "url": "https://www.ft.com/__origami/service/image/v2/images/raw/https%3A%2F%2Fd1e00ek4ebabms.cloudfront.net%2Fproduction%2F83847487-b048-46d2-9dd7-b4465710c740.jpg?source=next&fit=scale-down&dpr=2&width=340",
            "type": "primary",
            "mediaType": "image/jpeg"
        }],
    },

    {
        "id": "article5",
        "title": {
            "title": "Tech knowhow gives new lease of life to marine habitats"
        },
        "location": {
            "uri": "https://www.ft.com/content/6f6b60b3-9dd3-42c3-a5e7-6cf61863759b"
        },
        "images": [{
            "url": "https://www.ft.com/__origami/service/image/v2/images/raw/https%3A%2F%2Fd1e00ek4ebabms.cloudfront.net%2Fproduction%2F209f9fac-0705-4661-9265-35669a5db625.jpg?source=next&fit=scale-down&dpr=2&width=340",
            "type": "primary",
            "mediaType": "image/jpeg"
        }],

    },

    {
        "id": "article6",
        "title": {
            "title": "To save the planet, ask the locals"
        },
        "location": {
            "uri": "https://www.ft.com/content/5e0d475f-f8d0-4f86-873b-97e9ec5504f0"
        },
        "images": [{
            "url": "https://www.ft.com/__origami/service/image/v2/images/raw/https%3A%2F%2Fd1e00ek4ebabms.cloudfront.net%2Fproduction%2F9128f911-6d94-4a3e-b3d0-c8f3d706d7d9.jpg?source=next&fit=scale-down&dpr=2&width=340",
            "type": "primary",
            "mediaType": "image/jpeg"
        }],

    }]
};

ftSuiteConfig.exitClickHandler = function(id, url) {
    switch (id) {

        case "article1":
            Enabler.exitOverride("article1",
                "https://www.ft.com/content/7d940587-4502-4468-acea-a67b7bf6a523"
            );
            break;

        case "article2":
            Enabler.exitOverride("article2",
                "https://www.ft.com/content/b4a112dd-cafd-4522-bf79-9e25704577ab"
            );
            break;

        case "article3":
            Enabler.exitOverride("article3",
                "https://www.ft.com/content/4f807d17-2f95-4572-a7f4-50655fdda00e"
            );
            break;

        case "article4":
            Enabler.exitOverride(
                "article4",
                "https://www.ft.com/content/100f0c5b-83c5-4e9a-8ad0-89af2ea4a758"
            );
            break;

        case "article5":
            Enabler.exitOverride("article5",
                "https://www.ft.com/content/6f6b60b3-9dd3-42c3-a5e7-6cf61863759b"
            );
            break;

        case "article6":
            Enabler.exitOverride("article6",
                "https://www.ft.com/content/5e0d475f-f8d0-4f86-873b-97e9ec5504f0"
            );
            break;
    }
};
