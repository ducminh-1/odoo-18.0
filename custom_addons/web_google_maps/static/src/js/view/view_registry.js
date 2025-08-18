/** @odoo-module **/

import { registry } from "@web/core/registry";
import { GoogleMapView } from "./google_map/google_map_view"; // OWL component bạn viết

const viewRegistry = registry.category("views");
viewRegistry.add("google_map", GoogleMapView);


console.log('=====================', GoogleMapView);