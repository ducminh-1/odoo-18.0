/** @odoo-module **/

import { registry } from "@web/core/registry";
import { AbstractModel } from "@web/views/abstract_model";

export class GoogleMapModel extends AbstractModel {
    async load(params) {
        console.log("✅ GoogleMapModel.load called", params);
        return super.load(params);
    }

    async reload(handle, params) {
        console.log("♻️ GoogleMapModel.reload called", handle, params);
        return super.reload(handle, params);
    }
}

registry.category("models").add("google_map", GoogleMapModel);