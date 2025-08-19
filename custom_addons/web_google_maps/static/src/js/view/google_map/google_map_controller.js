/** @odoo-module **/

import { AbstractController } from "@web/views/abstract_controller";
import { registry } from "@web/core/registry";

export class GoogleMapController extends AbstractController {
    setup() {
        super.setup();
        console.log("✅ GoogleMapController setup");
    }

    async onClickRefresh() {
        console.log("🔄 Refresh Google Map view");
        await this.model.reload();
    }
}

registry.category("controllers").add("google_map", GoogleMapController);