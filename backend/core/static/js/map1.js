(function ($) {
    "use strict";
    mapboxgl.accessToken =
        "pk.eyJ1IjoiaG9hbmdoYW5kbiIsImEiOiJjbTdsbTkydm8wZGpiMmxxcTdvdzVqbHd3In0.HUUli-jvI1ALTBuzSeKTpw"; 

    const officeCoordinates = [-87.4548, 41.6389];

    const map = new mapboxgl.Map({
        container: "map",
        style: "mapbox://styles/mapbox/light-v11",
        center: officeCoordinates,
        zoom: 14,
    });

    map.on("load", () => {
        const markerElement = document.createElement("div");
        markerElement.className = "office-marker";
        markerElement.innerHTML = `<i class="icon-HouseLine"></i>`;

        const popupContent = `
            <div class="office-popup">
                <div class="text-title text_primary-color fw-6 mb_4">My Office</div>
                <p>101 E 129th St, East Chicago, 2nd Floor, NY</p>
            </div>
        `;

        const popup = new mapboxgl.Popup({
            closeButton: true,
            closeOnClick: false,
            offset: [0, -50],
        }).setHTML(popupContent);

        new mapboxgl.Marker({
            element: markerElement,
            anchor: "bottom",
        })
        .setLngLat(officeCoordinates)
        .setPopup(popup)
        .addTo(map);

        

        map.addControl(new mapboxgl.NavigationControl(), "top-right");
        map.addControl(new mapboxgl.FullscreenControl(), "top-right");
    });
})(this.jQuery);
