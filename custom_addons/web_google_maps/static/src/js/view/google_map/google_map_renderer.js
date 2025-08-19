/** @odoo-module **/

import { Component, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { qweb } from "@web/core/qweb";
import { session } from "@web/session";
import { loadJS, loadCSS } from "@web/core/assets";   // thay thế cho utils

export class GoogleMapRenderer extends Component {
    setup() {
        console.log("✅ GoogleMapRenderer setup loaded", session.uid);

        onMounted(async () => {
            await this._loadGoogleMap();
            this._renderMap();
        });
    }

    async _loadGoogleMap() {
        if (!window.google || !window.google.maps) {
            await loadJS("https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY");
        }
    }

    _renderMap() {
        const container = this.el.querySelector(".o_google_map_container");
        if (container && window.google) {
            const map = new google.maps.Map(container, {
                center: { lat: 21.0285, lng: 105.8542 }, // Hà Nội
                zoom: 12,
            });

            new google.maps.Marker({
                position: { lat: 21.0285, lng: 105.8542 },
                map,
                title: "Hello Google Maps!",
            });
        }
    }
}

GoogleMapRenderer.template = "web_google_maps.GoogleMapRendererTemplate";

// Đăng ký renderer
registry.category("views").add("google_map", {
    type: "google_map",
    display_name: "Google Map",
    icon: "fa fa-map",
    component: GoogleMapRenderer,
});
