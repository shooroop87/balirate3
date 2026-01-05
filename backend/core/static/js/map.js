(function ($) {
    "use strict";

    mapboxgl.accessToken = "pk.eyJ1IjoiaG9hbmdoYW5kbiIsImEiOiJjbTdsbTkydm8wZGpiMmxxcTdvdzVqbHd3In0.HUUli-jvI1ALTBuzSeKTpw";

    const map = new mapboxgl.Map({
        container: "map",
        style: "mapbox://styles/mapbox/light-v10",
        center: [-122.4194, 37.7749],
        zoom: 13,
        cooperativeGestures: true,
    });

    const properties = [
        {
            id: 1,
            address: "245 Elm Street, San Francisco, CA 94102",
            title: "Sunset Heights Estate",
            beds: 3,
            Bathss: 2,
            sqft: 1600,
            coordinates: [-122.4194, 37.7749],
            image: "/images/home/popup-property-1.jpg",
        },
        {
            id: 2,
            address: "72 Sunset Avenue, Los Angeles, California",
            title: "Villa del Mar Retreat, Malibu",
            beds: 4,
            Bathss: 2,
            sqft: 2400,
            coordinates: [-122.4094, 37.7849],
            image: "/images/home/popup-property-2.jpg",
        },
        {
            id: 3,
            address: "245 Elm Street, San Francisco, CA 94102",
            title: "Sunset Heights Estate",
            beds: 3,
            Bathss: 2,
            sqft: 1600,
            coordinates: [-122.4294, 37.7649],
            image: "/images/home/popup-property-3.jpg",
        },
        {
            id: 4,
            address: "918 Maple Avenue, Brooklyn, NY 11215",
            title: "Coastal Serenity Cottage",
            beds: 4,
            Bathss: 2,
            sqft: 2600,
            coordinates: [-122.4154, 37.7929],
            image: "/images/home/popup-property-4.jpg",
        },
        {
            id: 5,
            address: "456 Pacific Heights, San Francisco, CA 94115",
            title: "Elegant Townhouse",
            beds: 5,
            Bathss: 4,
            sqft: 2800,
            coordinates: [-122.4394, 37.7889],
            image: "/images/home/popup-property-5.jpg",
        },
        {
            id: 6,
            address: "77 Lakeview Court, Orlando, FL 32801",
            title: "Rancho Vista Verde",
            beds: 2,
            Bathss: 1,
            sqft: 900,
            coordinates: [-122.4494, 37.7719],
            image: "/images/home/popup-property-6.jpg",
        },
        {
            id: 7,
            address: "1422 Sunset Avenue, Los Angeles, CA 90026",
            title: "Palmcrest Residences",
            beds: 3,
            Bathss: 3,
            sqft: 1200,
            coordinates: [-122.4044, 37.7699],
            image: "/images/home/popup-property-7.jpg",
        },
        {
            id: 8,
            address: "456 Pacific Heights, San Francisco, CA 94115",
            title: "Elegant Townhouse",
            beds: 5,
            Bathss: 4,
            sqft: 2800,
            coordinates: [-122.4394, 37.7611],
            image: "/images/home/popup-property-8.jpg",
        },
        {
            id: 9,
            address: "91 Coastal Breeze Drive, San Diego, CA 92101",
            title: "Oceanview Heights",
            beds: 4,
            Bathss: 2,
            sqft: 2200,
            coordinates: [-122.4494, 37.7511],
            image: "/images/home/popup-property-9.jpg",
        },
    ];

    const geoData = {
        type: "FeatureCollection",
        features: properties.map((property) => ({
            type: "Feature",
            properties: {
                property_id: property.id.toString(),
                ...property,
            },
            geometry: {
                type: "Point",
                coordinates: property.coordinates,
            },
        })),
    };

    let currentPopup = null;

    properties.forEach((property) => {
        const markerElement = document.createElement("div");
        markerElement.className = "office-marker";
        markerElement.innerHTML = `<i class="icon-HouseLine"></i>`;

        const marker = new mapboxgl.Marker(markerElement)
            .setLngLat(property.coordinates)
            .addTo(map);

        markerElement.addEventListener("click", () => {
            if (currentPopup) currentPopup.remove();

            document.querySelectorAll(".office-marker").forEach((m) =>
                m.classList.remove("active")
            );
            markerElement.classList.add("active");

            const popupContent = `
            <div class="popup-property">
                <div class="img-style">
                    <img src="${property.image}" width="120" height="120" alt="popup-property">
                </div>
                <div class="content">
                    <p class="text-caption-1 mb_4">${property.address}</p>
                    <h6 class="mb_12">${property.title}</h6>
                    <ul class="info d-flex">
                        <li class="d-flex align-items-center gap_8 text_primary-color fw-6">
                            <i class="icon-Bed"></i>${property.beds} Bed
                        </li>
                        <li class="d-flex align-items-center gap_8 text_primary-color fw-6">
                            <i class="icon-Bathstub"></i>${property.Bathss} Baths
                        </li>
                        <li class="d-flex align-items-center gap_8 text_primary-color fw-6">
                            <i class="icon-Ruler"></i>${property.sqft} sqft
                        </li>
                    </ul>
                </div>
            </div>`;

            // 👉 Fly to property location
            map.flyTo({
                center: property.coordinates,
                zoom: 14,
                speed: 1.2,
                curve: 1,
                easing: (t) => t,
            });

            currentPopup = new mapboxgl.Popup({
                closeButton: false,
                closeOnClick: false,
                anchor: "bottom",
                offset: [0, -50],
            })
                .setLngLat(property.coordinates)
                .setHTML(popupContent)
                .addTo(map);
        });
    });

    function jumpToProperty(map, feature) {
        const [lng, lat] = feature.geometry.coordinates;
        map.flyTo({ center: [lng, lat], zoom: 14, speed: 1.2 });
    }

    function createPopupMap(map, feature) {
        const prop = feature.properties;

        const popupContent = `
        <div class="popup-property">
            <div class="img-style">
                <img src="${prop.image}" width="120" height="120" alt="popup-property">
            </div>
            <div class="content">
                <p class="text-caption-1 mb_4">${prop.address}</p>
                <h6 class="mb_12">${prop.title}</h6>
                <ul class="info d-flex">
                    <li class="d-flex align-items-center gap_8 text_primary-color fw-6">
                        <i class="icon-Bed"></i>${prop.beds} Bed
                    </li>
                    <li class="d-flex align-items-center gap_8 text_primary-color fw-6">
                        <i class="icon-Bathstub"></i>${prop.Bathss} Baths
                    </li>
                    <li class="d-flex align-items-center gap_8 text_primary-color fw-6">
                        <i class="icon-Ruler"></i>${prop.sqft} sqft
                    </li>
                </ul>
            </div>
        </div>`;

        if (currentPopup) currentPopup.remove();

        currentPopup = new mapboxgl.Popup({
            closeButton: false,
            closeOnClick: false,
            anchor: "bottom",
            offset: [0, -50],
        })
            .setLngLat(feature.geometry.coordinates)
            .setHTML(popupContent)
            .addTo(map);
    }

    function mouseoverPropertyMapBox(map, geoData) {
        $(".card-house").on("mouseover", function () {
            const dataId = $(this).attr("data-id");
            for (const feature of geoData.features) {
                if (feature.properties.property_id === dataId) {
                    jumpToProperty(map, feature);
                    createPopupMap(map, feature);
                }
            }
        });
    }

    map.on("load", function () {
        mouseoverPropertyMapBox(map, geoData);
    });

    map.on("click", (e) => {
        if (!e.originalEvent.target.closest(".office-marker")) {
            if (currentPopup) {
                currentPopup.remove();
                currentPopup = null;
            }
        }
    });

    map.addControl(new mapboxgl.NavigationControl(), "top-right");
    map.addControl(new mapboxgl.FullscreenControl(), "top-right");
    map.addControl(
        new mapboxgl.GeolocateControl({
            positionOptions: { enableHighAccuracy: true },
            trackUserLocation: true,
            showUserHeading: true,
        }),
        "top-right"
    );
})(jQuery);
