/**@odoo-module*/

import { registry } from '@web/core/registry';
const { Component } = owl

// Define the ProjectDashboard component
export class ProjectDashboard extends Component {
    // Future logic for the component can be added here
}

// Specify the template for the component
ProjectDashboard.template = "ProjectDashboardMain"

// Register the component in the actions category
registry.category("actions").add("project_dashboard_main", ProjectDashboard)
