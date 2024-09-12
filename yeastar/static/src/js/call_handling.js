/**@odoo-module*/

const { Component } = owl

import { useService } from "@web/core/utils/hooks";

export class IncomingCallDialog extends Component {
    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
    }

    async answerCall() {
        await this.orm.call(
            "incoming.call.log",
            "action_confirm",
            [this.props.data.id]
        );
        this.notification.add(this.env._t("Call answered"), {
            type: "success",
        });
        this.props.close();
    }

    async refuseCall() {
        await this.orm.call(
            "incoming.call.log",
            "action_refuse_call",
            [this.props.data.id]
        );
        this.notification.add(this.env._t("Call refused"), {
            type: "info",
        });
        this.props.close();
    }
}

IncomingCallDialog.template = "IncomingCallDialog";
