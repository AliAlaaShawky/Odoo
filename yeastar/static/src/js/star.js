/** @odoo-module **/

import { Component, onMounted, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class YeastarLeadCreation extends Component {
    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        console.log("Custom JavaScript for URL checking loaded!");
        this.state = useState({
            urlFragment: window.location.hash,
        });

        // Handle the URL change event on component mount
        onMounted(() => {
            console.log("Yeastar URL detected! Taking action...");
            window.addEventListener('hashchange', this.checkForYeastarURL.bind(this));
            this.checkForYeastarURL();  // Call it initially
        });
    }

    checkForYeastarURL() {
        const urlFragment = window.location.hash;
        if (urlFragment.includes('model=res.partner') && !urlFragment.includes('menu_id')) {
            console.log("Yeastar URL detected! Fetching contact details...");
            this.fetchContactAndCreateLead();
        }
    }

    async fetchContactAndCreateLead() {
        const contactID = this.extractContactIDFromURL();
        if (contactID) {
            try {
                // Fetch contact details (like phone number) using the contact ID
                const contact = await this.orm.read('res.partner', [parseInt(contactID)], ['phone', 'name']);

                if (contact && contact.length > 0) {
                    const contactDetails = contact[0];
                    const calleeNumber = contactDetails.phone;
                    const contactName = contactDetails.name;

                    if (calleeNumber) {
                        // Create a lead with the fetched contact details
                        const result = await this.orm.create('crm.lead', [{
                            name: `New Lead for ${contactName}`,  // Lead title
                            phone: calleeNumber,                  // Callee's phone number
                            description: 'Lead created from Yeastar URL check.',
                        }]);

                        console.log('Lead created successfully with ID:', result);
                        this.notification.add(`Lead created successfully for ${contactName}`, { type: 'success' });
                    } else {
                        this.notification.add('No phone number found for the contact.', { type: 'warning' });
                    }
                }
            } catch (error) {
                console.error('Error while fetching contact or creating lead:', error);
                this.notification.add('Error while creating lead.', { type: 'danger' });
            }
        }
    }

    extractContactIDFromURL() {
        const urlFragment = window.location.hash;
        const regex = /id=(\d+)/;  // Extract the ID from the URL fragment
        const match = urlFragment.match(regex);
        return match ? match[1] : null;
    }
}

YeastarLeadCreation.template = 'yeastar.YeastarLeadCreation';
