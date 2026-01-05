(function ($) {
    "use strict";

    mapboxgl.accessToken =
        "pk.eyJ1IjoiaG9hbmdoYW5kbiIsImEiOiJjbTdsbTkydm8wZGpiMmxxcTdvdzVqbHd3In0.HUUli-jvI1ALTBuzSeKTpw";

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

            document
                .querySelectorAll(".office-marker")
                .forEach((m) => m.classList.remove("active"));
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
        map.resize(); 
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
