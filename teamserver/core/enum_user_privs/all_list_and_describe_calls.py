all_list_and_describe_calls_dict = {
    "s3": {
        "List": [
            "list_bucket_analytics_configurations",
            "list_bucket_intelligent_tiering_configurations",
            "list_bucket_inventory_configurations",
            "list_bucket_metrics_configurations",
            "list_buckets",
            "list_multipart_uploads",
            "list_object_versions",
            "list_objects",
            "list_objects_v2",
            "list_parts"
        ],
        "Describe": []
    },
    "ec2": {
        "List": [],
        "Describe": [
            "describe_account_attributes",
            "describe_addresses",
            "describe_addresses_attribute",
            "describe_aggregate_id_format",
            "describe_availability_zones",
            "describe_bundle_tasks",
            "describe_byoip_cidrs",
            "describe_capacity_reservation_fleets",
            "describe_capacity_reservations",
            "describe_carrier_gateways",
            "describe_classic_link_instances",
            "describe_client_vpn_authorization_rules",
            "describe_client_vpn_connections",
            "describe_client_vpn_endpoints",
            "describe_client_vpn_routes",
            "describe_client_vpn_target_networks",
            "describe_coip_pools",
            "describe_conversion_tasks",
            "describe_customer_gateways",
            "describe_dhcp_options",
            "describe_egress_only_internet_gateways",
            "describe_elastic_gpus",
            "describe_export_image_tasks",
            "describe_export_tasks",
            "describe_fast_snapshot_restores",
            "describe_fleet_history",
            "describe_fleet_instances",
            "describe_fleets",
            "describe_flow_logs",
            "describe_fpga_image_attribute",
            "describe_fpga_images",
            "describe_host_reservation_offerings",
            "describe_host_reservations",
            "describe_hosts",
            "describe_iam_instance_profile_associations",
            "describe_id_format",
            "describe_identity_id_format",
            "describe_image_attribute",
            "describe_images",
            "describe_import_image_tasks",
            "describe_import_snapshot_tasks",
            "describe_instance_attribute",
            "describe_instance_credit_specifications",
            "describe_instance_event_notification_attributes",
            "describe_instance_event_windows",
            "describe_instance_status",
            "describe_instance_type_offerings",
            "describe_instance_types",
            "describe_instances",
            "describe_internet_gateways",
            "describe_ipv6_pools",
            "describe_key_pairs",
            "describe_launch_template_versions",
            "describe_launch_templates",
            "describe_local_gateway_route_table_virtual_interface_group_associations",
            "describe_local_gateway_route_table_vpc_associations",
            "describe_local_gateway_route_tables",
            "describe_local_gateway_virtual_interface_groups",
            "describe_local_gateway_virtual_interfaces",
            "describe_local_gateways",
            "describe_managed_prefix_lists",
            "describe_moving_addresses",
            "describe_nat_gateways",
            "describe_network_acls",
            "describe_network_insights_analyses",
            "describe_network_insights_paths",
            "describe_network_interface_attribute",
            "describe_network_interface_permissions",
            "describe_network_interfaces",
            "describe_placement_groups",
            "describe_prefix_lists",
            "describe_principal_id_format",
            "describe_public_ipv4_pools",
            "describe_regions",
            "describe_replace_root_volume_tasks",
            "describe_reserved_instances",
            "describe_reserved_instances_listings",
            "describe_reserved_instances_modifications",
            "describe_reserved_instances_offerings",
            "describe_route_tables",
            "describe_scheduled_instance_availability",
            "describe_scheduled_instances",
            "describe_security_group_references",
            "describe_security_group_rules",
            "describe_security_groups",
            "describe_snapshot_attribute",
            "describe_snapshots",
            "describe_spot_datafeed_subscription",
            "describe_spot_fleet_instances",
            "describe_spot_fleet_request_history",
            "describe_spot_fleet_requests",
            "describe_spot_instance_requests",
            "describe_spot_price_history",
            "describe_stale_security_groups",
            "describe_store_image_tasks",
            "describe_subnets",
            "describe_tags",
            "describe_traffic_mirror_filters",
            "describe_traffic_mirror_sessions",
            "describe_traffic_mirror_targets",
            "describe_transit_gateway_attachments",
            "describe_transit_gateway_connect_peers",
            "describe_transit_gateway_connects",
            "describe_transit_gateway_multicast_domains",
            "describe_transit_gateway_peering_attachments",
            "describe_transit_gateway_route_tables",
            "describe_transit_gateway_vpc_attachments",
            "describe_transit_gateways",
            "describe_trunk_interface_associations",
            "describe_volume_attribute",
            "describe_volume_status",
            "describe_volumes",
            "describe_volumes_modifications",
            "describe_vpc_attribute",
            "describe_vpc_classic_link",
            "describe_vpc_classic_link_dns_support",
            "describe_vpc_endpoint_connection_notifications",
            "describe_vpc_endpoint_connections",
            "describe_vpc_endpoint_service_configurations",
            "describe_vpc_endpoint_service_permissions",
            "describe_vpc_endpoint_services",
            "describe_vpc_endpoints",
            "describe_vpc_peering_connections",
            "describe_vpcs",
            "describe_vpn_connections",
            "describe_vpn_gateways"
        ]
    },
    "iam": {
        "List": [
            "list_access_keys",
            "list_account_aliases",
            "list_attached_group_policies",
            "list_attached_role_policies",
            "list_attached_user_policies",
            "list_entities_for_policy",
            "list_group_policies",
            "list_groups",
            "list_groups_for_user",
            "list_instance_profile_tags",
            "list_instance_profiles",
            "list_instance_profiles_for_role",
            "list_mfa_device_tags",
            "list_mfa_devices",
            "list_open_id_connect_provider_tags",
            "list_open_id_connect_providers",
            "list_policies",
            "list_policies_granting_service_access",
            "list_policy_tags",
            "list_policy_versions",
            "list_role_policies",
            "list_role_tags",
            "list_roles",
            "list_saml_provider_tags",
            "list_saml_providers",
            "list_server_certificate_tags",
            "list_server_certificates",
            "list_service_specific_credentials",
            "list_signing_certificates",
            "list_ssh_public_keys",
            "list_user_policies",
            "list_user_tags",
            "list_users",
            "list_virtual_mfa_devices"
        ],
        "Describe": []
    },
    "sts": {
        "List": [],
        "Describe": []
    },
    "lambda": {
        "List": [
            "list_aliases",
            "list_code_signing_configs",
            "list_event_source_mappings",
            "list_function_event_invoke_configs",
            "list_functions",
            "list_functions_by_code_signing_config",
            "list_layer_versions",
            "list_layers",
            "list_provisioned_concurrency_configs",
            "list_tags",
            "list_versions_by_function"
        ],
        "Describe": []
    },
    "ecr": {
        "List": [
            "list_images",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_image_replication_status",
            "describe_image_scan_findings",
            "describe_images",
            "describe_registry",
            "describe_repositories"
        ]
    },
    "eks": {
        "List": [
            "list_addons",
            "list_clusters",
            "list_fargate_profiles",
            "list_identity_provider_configs",
            "list_nodegroups",
            "list_tags_for_resource",
            "list_updates"
        ],
        "Describe": [
            "describe_addon",
            "describe_addon_versions",
            "describe_cluster",
            "describe_fargate_profile",
            "describe_identity_provider_config",
            "describe_nodegroup",
            "describe_update"
        ]
    },
    "accessanalyzer": {
        "List": [
            "list_access_preview_findings",
            "list_access_previews",
            "list_analyzed_resources",
            "list_analyzers",
            "list_archive_rules",
            "list_findings",
            "list_policy_generations",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "acm": {
        "List": [
            "list_certificates",
            "list_tags_for_certificate"
        ],
        "Describe": [
            "describe_certificate"
        ]
    },
    "acm-pca": {
        "List": [
            "list_certificate_authorities",
            "list_permissions",
            "list_tags"
        ],
        "Describe": [
            "describe_certificate_authority",
            "describe_certificate_authority_audit_report"
        ]
    },
    "alexaforbusiness": {
        "List": [
            "list_business_report_schedules",
            "list_conference_providers",
            "list_device_events",
            "list_gateway_groups",
            "list_gateways",
            "list_skills",
            "list_skills_store_categories",
            "list_skills_store_skills_by_category",
            "list_smart_home_appliances",
            "list_tags"
        ],
        "Describe": []
    },
    "amp": {
        "List": [
            "list_rule_groups_namespaces",
            "list_tags_for_resource",
            "list_workspaces"
        ],
        "Describe": [
            "describe_alert_manager_definition",
            "describe_rule_groups_namespace",
            "describe_workspace"
        ]
    },
    "amplify": {
        "List": [
            "list_apps",
            "list_artifacts",
            "list_backend_environments",
            "list_branches",
            "list_domain_associations",
            "list_jobs",
            "list_tags_for_resource",
            "list_webhooks"
        ],
        "Describe": []
    },
    "amplifybackend": {
        "List": [
            "list_backend_jobs"
        ],
        "Describe": []
    },
    "apigateway": {
        "List": [],
        "Describe": []
    },
    "apigatewaymanagementapi": {
        "List": [],
        "Describe": []
    },
    "apigatewayv2": {
        "List": [],
        "Describe": []
    },
    "appconfig": {
        "List": [
            "list_applications",
            "list_configuration_profiles",
            "list_deployment_strategies",
            "list_deployments",
            "list_environments",
            "list_hosted_configuration_versions",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "appflow": {
        "List": [
            "list_connector_entities",
            "list_flows",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_connector_entity",
            "describe_connector_profiles",
            "describe_connectors",
            "describe_flow",
            "describe_flow_execution_records"
        ]
    },
    "appintegrations": {
        "List": [
            "list_data_integration_associations",
            "list_data_integrations",
            "list_event_integration_associations",
            "list_event_integrations",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "application-autoscaling": {
        "List": [],
        "Describe": [
            "describe_scalable_targets",
            "describe_scaling_activities",
            "describe_scaling_policies",
            "describe_scheduled_actions"
        ]
    },
    "application-insights": {
        "List": [
            "list_applications",
            "list_components",
            "list_configuration_history",
            "list_log_pattern_sets",
            "list_log_patterns",
            "list_problems",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_application",
            "describe_component",
            "describe_component_configuration",
            "describe_component_configuration_recommendation",
            "describe_log_pattern",
            "describe_observation",
            "describe_problem",
            "describe_problem_observations"
        ]
    },
    "applicationcostprofiler": {
        "List": [
            "list_report_definitions"
        ],
        "Describe": []
    },
    "appmesh": {
        "List": [
            "list_gateway_routes",
            "list_meshes",
            "list_routes",
            "list_tags_for_resource",
            "list_virtual_gateways",
            "list_virtual_nodes",
            "list_virtual_routers",
            "list_virtual_services"
        ],
        "Describe": [
            "describe_gateway_route",
            "describe_mesh",
            "describe_route",
            "describe_virtual_gateway",
            "describe_virtual_node",
            "describe_virtual_router",
            "describe_virtual_service"
        ]
    },
    "apprunner": {
        "List": [
            "list_auto_scaling_configurations",
            "list_connections",
            "list_operations",
            "list_services",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_auto_scaling_configuration",
            "describe_custom_domains",
            "describe_service"
        ]
    },
    "appstream": {
        "List": [
            "list_associated_fleets",
            "list_associated_stacks",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_directory_configs",
            "describe_fleets",
            "describe_image_builders",
            "describe_image_permissions",
            "describe_images",
            "describe_sessions",
            "describe_stacks",
            "describe_usage_report_subscriptions",
            "describe_user_stack_associations",
            "describe_users"
        ]
    },
    "appsync": {
        "List": [
            "list_api_keys",
            "list_data_sources",
            "list_functions",
            "list_graphql_apis",
            "list_resolvers",
            "list_resolvers_by_function",
            "list_tags_for_resource",
            "list_types"
        ],
        "Describe": []
    },
    "athena": {
        "List": [
            "list_data_catalogs",
            "list_databases",
            "list_engine_versions",
            "list_named_queries",
            "list_prepared_statements",
            "list_query_executions",
            "list_table_metadata",
            "list_tags_for_resource",
            "list_work_groups"
        ],
        "Describe": []
    },
    "auditmanager": {
        "List": [
            "list_assessment_frameworks",
            "list_assessment_reports",
            "list_assessments",
            "list_controls",
            "list_keywords_for_data_source",
            "list_notifications",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "autoscaling": {
        "List": [],
        "Describe": [
            "describe_account_limits",
            "describe_adjustment_types",
            "describe_auto_scaling_groups",
            "describe_auto_scaling_instances",
            "describe_auto_scaling_notification_types",
            "describe_instance_refreshes",
            "describe_launch_configurations",
            "describe_lifecycle_hook_types",
            "describe_lifecycle_hooks",
            "describe_load_balancer_target_groups",
            "describe_load_balancers",
            "describe_metric_collection_types",
            "describe_notification_configurations",
            "describe_policies",
            "describe_scaling_activities",
            "describe_scaling_process_types",
            "describe_scheduled_actions",
            "describe_tags",
            "describe_termination_policy_types",
            "describe_warm_pool"
        ]
    },
    "autoscaling-plans": {
        "List": [],
        "Describe": [
            "describe_scaling_plan_resources",
            "describe_scaling_plans"
        ]
    },
    "backup": {
        "List": [
            "list_backup_jobs",
            "list_backup_plan_templates",
            "list_backup_plan_versions",
            "list_backup_plans",
            "list_backup_selections",
            "list_backup_vaults",
            "list_copy_jobs",
            "list_frameworks",
            "list_protected_resources",
            "list_recovery_points_by_backup_vault",
            "list_recovery_points_by_resource",
            "list_report_jobs",
            "list_report_plans",
            "list_restore_jobs",
            "list_tags"
        ],
        "Describe": [
            "describe_backup_job",
            "describe_backup_vault",
            "describe_copy_job",
            "describe_framework",
            "describe_global_settings",
            "describe_protected_resource",
            "describe_recovery_point",
            "describe_region_settings",
            "describe_report_job",
            "describe_report_plan",
            "describe_restore_job"
        ]
    },
    "batch": {
        "List": [
            "list_jobs",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_compute_environments",
            "describe_job_definitions",
            "describe_job_queues",
            "describe_jobs"
        ]
    },
    "braket": {
        "List": [
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "budgets": {
        "List": [],
        "Describe": [
            "describe_budget",
            "describe_budget_action",
            "describe_budget_action_histories",
            "describe_budget_actions_for_account",
            "describe_budget_actions_for_budget",
            "describe_budget_performance_history",
            "describe_budgets",
            "describe_notifications_for_budget",
            "describe_subscribers_for_notification"
        ]
    },
    "ce": {
        "List": [
            "list_cost_category_definitions"
        ],
        "Describe": [
            "describe_cost_category_definition"
        ]
    },
    "chime": {
        "List": [
            "list_accounts",
            "list_app_instance_admins",
            "list_app_instance_users",
            "list_app_instances",
            "list_attendee_tags",
            "list_attendees",
            "list_bots",
            "list_channel_bans",
            "list_channel_memberships",
            "list_channel_memberships_for_app_instance_user",
            "list_channel_messages",
            "list_channel_moderators",
            "list_channels",
            "list_channels_moderated_by_app_instance_user",
            "list_media_capture_pipelines",
            "list_meeting_tags",
            "list_meetings",
            "list_phone_number_orders",
            "list_phone_numbers",
            "list_proxy_sessions",
            "list_room_memberships",
            "list_rooms",
            "list_sip_media_applications",
            "list_sip_rules",
            "list_supported_phone_number_countries",
            "list_tags_for_resource",
            "list_users",
            "list_voice_connector_groups",
            "list_voice_connector_termination_credentials",
            "list_voice_connectors"
        ],
        "Describe": [
            "describe_app_instance",
            "describe_app_instance_admin",
            "describe_app_instance_user",
            "describe_channel",
            "describe_channel_ban",
            "describe_channel_membership",
            "describe_channel_membership_for_app_instance_user",
            "describe_channel_moderated_by_app_instance_user",
            "describe_channel_moderator"
        ]
    },
    "cloud9": {
        "List": [
            "list_environments",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_environment_memberships",
            "describe_environment_status",
            "describe_environments"
        ]
    },
    "clouddirectory": {
        "List": [
            "list_applied_schema_arns",
            "list_attached_indices",
            "list_development_schema_arns",
            "list_directories",
            "list_facet_attributes",
            "list_facet_names",
            "list_incoming_typed_links",
            "list_index",
            "list_managed_schema_arns",
            "list_object_attributes",
            "list_object_children",
            "list_object_parent_paths",
            "list_object_parents",
            "list_object_policies",
            "list_outgoing_typed_links",
            "list_policy_attachments",
            "list_published_schema_arns",
            "list_tags_for_resource",
            "list_typed_link_facet_attributes",
            "list_typed_link_facet_names"
        ],
        "Describe": []
    },
    "cloudformation": {
        "List": [
            "list_change_sets",
            "list_exports",
            "list_imports",
            "list_stack_instances",
            "list_stack_resources",
            "list_stack_set_operation_results",
            "list_stack_set_operations",
            "list_stack_sets",
            "list_stacks",
            "list_type_registrations",
            "list_type_versions",
            "list_types"
        ],
        "Describe": [
            "describe_account_limits",
            "describe_change_set",
            "describe_publisher",
            "describe_stack_drift_detection_status",
            "describe_stack_events",
            "describe_stack_instance",
            "describe_stack_resource",
            "describe_stack_resource_drifts",
            "describe_stack_resources",
            "describe_stack_set",
            "describe_stack_set_operation",
            "describe_stacks",
            "describe_type",
            "describe_type_registration"
        ]
    },
    "cloudfront": {
        "List": [
            "list_cache_policies",
            "list_cloud_front_origin_access_identities",
            "list_conflicting_aliases",
            "list_distributions",
            "list_distributions_by_cache_policy_id",
            "list_distributions_by_key_group",
            "list_distributions_by_origin_request_policy_id",
            "list_distributions_by_realtime_log_config",
            "list_distributions_by_web_acl_id",
            "list_field_level_encryption_configs",
            "list_field_level_encryption_profiles",
            "list_functions",
            "list_invalidations",
            "list_key_groups",
            "list_origin_request_policies",
            "list_public_keys",
            "list_realtime_log_configs",
            "list_streaming_distributions",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_function"
        ]
    },
    "cloudhsm": {
        "List": [
            "list_available_zones",
            "list_hapgs",
            "list_hsms",
            "list_luna_clients",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_hapg",
            "describe_hsm",
            "describe_luna_client"
        ]
    },
    "cloudhsmv2": {
        "List": [
            "list_tags"
        ],
        "Describe": [
            "describe_backups",
            "describe_clusters"
        ]
    },
    "cloudsearch": {
        "List": [
            "list_domain_names"
        ],
        "Describe": [
            "describe_analysis_schemes",
            "describe_availability_options",
            "describe_domain_endpoint_options",
            "describe_domains",
            "describe_expressions",
            "describe_index_fields",
            "describe_scaling_parameters",
            "describe_service_access_policies",
            "describe_suggesters"
        ]
    },
    "cloudsearchdomain": {
        "List": [],
        "Describe": []
    },
    "cloudtrail": {
        "List": [
            "list_public_keys",
            "list_tags",
            "list_trails"
        ],
        "Describe": [
            "describe_trails"
        ]
    },
    "cloudwatch": {
        "List": [
            "list_dashboards",
            "list_metric_streams",
            "list_metrics",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_alarm_history",
            "describe_alarms",
            "describe_alarms_for_metric",
            "describe_anomaly_detectors",
            "describe_insight_rules"
        ]
    },
    "codeartifact": {
        "List": [
            "list_domains",
            "list_package_version_assets",
            "list_package_version_dependencies",
            "list_package_versions",
            "list_packages",
            "list_repositories",
            "list_repositories_in_domain",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_domain",
            "describe_package_version",
            "describe_repository"
        ]
    },
    "codebuild": {
        "List": [
            "list_build_batches",
            "list_build_batches_for_project",
            "list_builds",
            "list_builds_for_project",
            "list_curated_environment_images",
            "list_projects",
            "list_report_groups",
            "list_reports",
            "list_reports_for_report_group",
            "list_shared_projects",
            "list_shared_report_groups",
            "list_source_credentials"
        ],
        "Describe": [
            "describe_code_coverages",
            "describe_test_cases"
        ]
    },
    "codecommit": {
        "List": [
            "list_approval_rule_templates",
            "list_associated_approval_rule_templates_for_repository",
            "list_branches",
            "list_pull_requests",
            "list_repositories",
            "list_repositories_for_approval_rule_template",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_merge_conflicts",
            "describe_pull_request_events"
        ]
    },
    "codedeploy": {
        "List": [
            "list_application_revisions",
            "list_applications",
            "list_deployment_configs",
            "list_deployment_groups",
            "list_deployment_instances",
            "list_deployment_targets",
            "list_deployments",
            "list_git_hub_account_token_names",
            "list_on_premises_instances",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "codeguru-reviewer": {
        "List": [
            "list_code_reviews",
            "list_recommendation_feedback",
            "list_recommendations",
            "list_repository_associations",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_code_review",
            "describe_recommendation_feedback",
            "describe_repository_association"
        ]
    },
    "codeguruprofiler": {
        "List": [
            "list_findings_reports",
            "list_profile_times",
            "list_profiling_groups",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_profiling_group"
        ]
    },
    "codepipeline": {
        "List": [
            "list_action_executions",
            "list_action_types",
            "list_pipeline_executions",
            "list_pipelines",
            "list_tags_for_resource",
            "list_webhooks"
        ],
        "Describe": []
    },
    "codestar": {
        "List": [
            "list_projects",
            "list_resources",
            "list_tags_for_project",
            "list_team_members",
            "list_user_profiles"
        ],
        "Describe": [
            "describe_project",
            "describe_user_profile"
        ]
    },
    "codestar-connections": {
        "List": [
            "list_connections",
            "list_hosts",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "codestar-notifications": {
        "List": [
            "list_event_types",
            "list_notification_rules",
            "list_tags_for_resource",
            "list_targets"
        ],
        "Describe": [
            "describe_notification_rule"
        ]
    },
    "cognito-identity": {
        "List": [
            "list_identities",
            "list_identity_pools",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_identity",
            "describe_identity_pool"
        ]
    },
    "cognito-idp": {
        "List": [
            "list_devices",
            "list_groups",
            "list_identity_providers",
            "list_resource_servers",
            "list_tags_for_resource",
            "list_user_import_jobs",
            "list_user_pool_clients",
            "list_user_pools",
            "list_users",
            "list_users_in_group"
        ],
        "Describe": [
            "describe_identity_provider",
            "describe_resource_server",
            "describe_risk_configuration",
            "describe_user_import_job",
            "describe_user_pool",
            "describe_user_pool_client",
            "describe_user_pool_domain"
        ]
    },
    "cognito-sync": {
        "List": [
            "list_datasets",
            "list_identity_pool_usage",
            "list_records"
        ],
        "Describe": [
            "describe_dataset",
            "describe_identity_pool_usage",
            "describe_identity_usage"
        ]
    },
    "comprehend": {
        "List": [
            "list_document_classification_jobs",
            "list_document_classifier_summaries",
            "list_document_classifiers",
            "list_dominant_language_detection_jobs",
            "list_endpoints",
            "list_entities_detection_jobs",
            "list_entity_recognizer_summaries",
            "list_entity_recognizers",
            "list_events_detection_jobs",
            "list_key_phrases_detection_jobs",
            "list_pii_entities_detection_jobs",
            "list_sentiment_detection_jobs",
            "list_tags_for_resource",
            "list_topics_detection_jobs"
        ],
        "Describe": [
            "describe_document_classification_job",
            "describe_document_classifier",
            "describe_dominant_language_detection_job",
            "describe_endpoint",
            "describe_entities_detection_job",
            "describe_entity_recognizer",
            "describe_events_detection_job",
            "describe_key_phrases_detection_job",
            "describe_pii_entities_detection_job",
            "describe_sentiment_detection_job",
            "describe_topics_detection_job"
        ]
    },
    "comprehendmedical": {
        "List": [
            "list_entities_detection_v2_jobs",
            "list_icd10_cm_inference_jobs",
            "list_phi_detection_jobs",
            "list_rx_norm_inference_jobs"
        ],
        "Describe": [
            "describe_entities_detection_v2_job",
            "describe_icd10_cm_inference_job",
            "describe_phi_detection_job",
            "describe_rx_norm_inference_job"
        ]
    },
    "compute-optimizer": {
        "List": [],
        "Describe": [
            "describe_recommendation_export_jobs"
        ]
    },
    "config": {
        "List": [
            "list_aggregate_discovered_resources",
            "list_discovered_resources",
            "list_stored_queries",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_aggregate_compliance_by_config_rules",
            "describe_aggregate_compliance_by_conformance_packs",
            "describe_aggregation_authorizations",
            "describe_compliance_by_config_rule",
            "describe_compliance_by_resource",
            "describe_config_rule_evaluation_status",
            "describe_config_rules",
            "describe_configuration_aggregator_sources_status",
            "describe_configuration_aggregators",
            "describe_configuration_recorder_status",
            "describe_configuration_recorders",
            "describe_conformance_pack_compliance",
            "describe_conformance_pack_status",
            "describe_conformance_packs",
            "describe_delivery_channel_status",
            "describe_delivery_channels",
            "describe_organization_config_rule_statuses",
            "describe_organization_config_rules",
            "describe_organization_conformance_pack_statuses",
            "describe_organization_conformance_packs",
            "describe_pending_aggregation_requests",
            "describe_remediation_configurations",
            "describe_remediation_exceptions",
            "describe_remediation_execution_status",
            "describe_retention_configurations"
        ]
    },
    "connect": {
        "List": [
            "list_agent_statuses",
            "list_approved_origins",
            "list_bots",
            "list_contact_flows",
            "list_hours_of_operations",
            "list_instance_attributes",
            "list_instance_storage_configs",
            "list_instances",
            "list_integration_associations",
            "list_lambda_functions",
            "list_lex_bots",
            "list_phone_numbers",
            "list_prompts",
            "list_queue_quick_connects",
            "list_queues",
            "list_quick_connects",
            "list_routing_profile_queues",
            "list_routing_profiles",
            "list_security_keys",
            "list_security_profiles",
            "list_tags_for_resource",
            "list_use_cases",
            "list_user_hierarchy_groups",
            "list_users"
        ],
        "Describe": [
            "describe_agent_status",
            "describe_contact_flow",
            "describe_hours_of_operation",
            "describe_instance",
            "describe_instance_attribute",
            "describe_instance_storage_config",
            "describe_queue",
            "describe_quick_connect",
            "describe_routing_profile",
            "describe_user",
            "describe_user_hierarchy_group",
            "describe_user_hierarchy_structure"
        ]
    },
    "connect-contact-lens": {
        "List": [
            "list_realtime_contact_analysis_segments"
        ],
        "Describe": []
    },
    "connectparticipant": {
        "List": [],
        "Describe": []
    },
    "cur": {
        "List": [],
        "Describe": [
            "describe_report_definitions"
        ]
    },
    "customer-profiles": {
        "List": [
            "list_account_integrations",
            "list_domains",
            "list_integrations",
            "list_profile_object_type_templates",
            "list_profile_object_types",
            "list_profile_objects",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "databrew": {
        "List": [
            "list_datasets",
            "list_job_runs",
            "list_jobs",
            "list_projects",
            "list_recipe_versions",
            "list_recipes",
            "list_schedules",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_dataset",
            "describe_job",
            "describe_job_run",
            "describe_project",
            "describe_recipe",
            "describe_schedule"
        ]
    },
    "dataexchange": {
        "List": [
            "list_data_set_revisions",
            "list_data_sets",
            "list_event_actions",
            "list_jobs",
            "list_revision_assets",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "datapipeline": {
        "List": [
            "list_pipelines"
        ],
        "Describe": [
            "describe_objects",
            "describe_pipelines"
        ]
    },
    "datasync": {
        "List": [
            "list_agents",
            "list_locations",
            "list_tags_for_resource",
            "list_task_executions",
            "list_tasks"
        ],
        "Describe": [
            "describe_agent",
            "describe_location_efs",
            "describe_location_fsx_windows",
            "describe_location_nfs",
            "describe_location_object_storage",
            "describe_location_s3",
            "describe_location_smb",
            "describe_task",
            "describe_task_execution"
        ]
    },
    "dax": {
        "List": [
            "list_tags"
        ],
        "Describe": [
            "describe_clusters",
            "describe_default_parameters",
            "describe_events",
            "describe_parameter_groups",
            "describe_parameters",
            "describe_subnet_groups"
        ]
    },
    "detective": {
        "List": [
            "list_graphs",
            "list_invitations",
            "list_members",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "devicefarm": {
        "List": [
            "list_artifacts",
            "list_device_instances",
            "list_device_pools",
            "list_devices",
            "list_instance_profiles",
            "list_jobs",
            "list_network_profiles",
            "list_offering_promotions",
            "list_offering_transactions",
            "list_offerings",
            "list_projects",
            "list_remote_access_sessions",
            "list_runs",
            "list_samples",
            "list_suites",
            "list_tags_for_resource",
            "list_test_grid_projects",
            "list_test_grid_session_actions",
            "list_test_grid_session_artifacts",
            "list_test_grid_sessions",
            "list_tests",
            "list_unique_problems",
            "list_uploads",
            "list_vpce_configurations"
        ],
        "Describe": []
    },
    "devops-guru": {
        "List": [
            "list_anomalies_for_insight",
            "list_events",
            "list_insights",
            "list_notification_channels",
            "list_recommendations"
        ],
        "Describe": [
            "describe_account_health",
            "describe_account_overview",
            "describe_anomaly",
            "describe_feedback",
            "describe_insight",
            "describe_resource_collection_health",
            "describe_service_integration"
        ]
    },
    "directconnect": {
        "List": [
            "list_virtual_interface_test_history"
        ],
        "Describe": [
            "describe_connection_loa",
            "describe_connections",
            "describe_connections_on_interconnect",
            "describe_direct_connect_gateway_association_proposals",
            "describe_direct_connect_gateway_associations",
            "describe_direct_connect_gateway_attachments",
            "describe_direct_connect_gateways",
            "describe_hosted_connections",
            "describe_interconnect_loa",
            "describe_interconnects",
            "describe_lags",
            "describe_loa",
            "describe_locations",
            "describe_tags",
            "describe_virtual_gateways",
            "describe_virtual_interfaces"
        ]
    },
    "discovery": {
        "List": [
            "list_configurations",
            "list_server_neighbors"
        ],
        "Describe": [
            "describe_agents",
            "describe_configurations",
            "describe_continuous_exports",
            "describe_export_configurations",
            "describe_export_tasks",
            "describe_import_tasks",
            "describe_tags"
        ]
    },
    "dlm": {
        "List": [
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "dms": {
        "List": [
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_account_attributes",
            "describe_applicable_individual_assessments",
            "describe_certificates",
            "describe_connections",
            "describe_endpoint_settings",
            "describe_endpoint_types",
            "describe_endpoints",
            "describe_event_categories",
            "describe_event_subscriptions",
            "describe_events",
            "describe_orderable_replication_instances",
            "describe_pending_maintenance_actions",
            "describe_refresh_schemas_status",
            "describe_replication_instance_task_logs",
            "describe_replication_instances",
            "describe_replication_subnet_groups",
            "describe_replication_task_assessment_results",
            "describe_replication_task_assessment_runs",
            "describe_replication_task_individual_assessments",
            "describe_replication_tasks",
            "describe_schemas",
            "describe_table_statistics"
        ]
    },
    "docdb": {
        "List": [
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_certificates",
            "describe_db_cluster_parameter_groups",
            "describe_db_cluster_parameters",
            "describe_db_cluster_snapshot_attributes",
            "describe_db_cluster_snapshots",
            "describe_db_clusters",
            "describe_db_engine_versions",
            "describe_db_instances",
            "describe_db_subnet_groups",
            "describe_engine_default_cluster_parameters",
            "describe_event_categories",
            "describe_event_subscriptions",
            "describe_events",
            "describe_global_clusters",
            "describe_orderable_db_instance_options",
            "describe_pending_maintenance_actions"
        ]
    },
    "ds": {
        "List": [
            "list_certificates",
            "list_ip_routes",
            "list_log_subscriptions",
            "list_schema_extensions",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_certificate",
            "describe_client_authentication_settings",
            "describe_conditional_forwarders",
            "describe_directories",
            "describe_domain_controllers",
            "describe_event_topics",
            "describe_ldaps_settings",
            "describe_regions",
            "describe_shared_directories",
            "describe_snapshots",
            "describe_trusts"
        ]
    },
    "dynamodb": {
        "List": [
            "list_backups",
            "list_contributor_insights",
            "list_exports",
            "list_global_tables",
            "list_tables",
            "list_tags_of_resource"
        ],
        "Describe": [
            "describe_backup",
            "describe_continuous_backups",
            "describe_contributor_insights",
            "describe_endpoints",
            "describe_export",
            "describe_global_table",
            "describe_global_table_settings",
            "describe_kinesis_streaming_destination",
            "describe_limits",
            "describe_table",
            "describe_table_replica_auto_scaling",
            "describe_time_to_live"
        ]
    },
    "dynamodbstreams": {
        "List": [
            "list_streams"
        ],
        "Describe": [
            "describe_stream"
        ]
    },
    "ebs": {
        "List": [
            "list_changed_blocks",
            "list_snapshot_blocks"
        ],
        "Describe": []
    },
    "ec2-instance-connect": {
        "List": [],
        "Describe": []
    },
    "ecr-public": {
        "List": [
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_image_tags",
            "describe_images",
            "describe_registries",
            "describe_repositories"
        ]
    },
    "ecs": {
        "List": [
            "list_account_settings",
            "list_attributes",
            "list_clusters",
            "list_container_instances",
            "list_services",
            "list_tags_for_resource",
            "list_task_definition_families",
            "list_task_definitions",
            "list_tasks"
        ],
        "Describe": [
            "describe_capacity_providers",
            "describe_clusters",
            "describe_container_instances",
            "describe_services",
            "describe_task_definition",
            "describe_task_sets",
            "describe_tasks"
        ]
    },
    "efs": {
        "List": [
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_access_points",
            "describe_account_preferences",
            "describe_backup_policy",
            "describe_file_system_policy",
            "describe_file_systems",
            "describe_lifecycle_configuration",
            "describe_mount_target_security_groups",
            "describe_mount_targets",
            "describe_tags"
        ]
    },
    "elastic-inference": {
        "List": [
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_accelerator_offerings",
            "describe_accelerator_types",
            "describe_accelerators"
        ]
    },
    "elasticache": {
        "List": [
            "list_allowed_node_type_modifications",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_cache_clusters",
            "describe_cache_engine_versions",
            "describe_cache_parameter_groups",
            "describe_cache_parameters",
            "describe_cache_security_groups",
            "describe_cache_subnet_groups",
            "describe_engine_default_parameters",
            "describe_events",
            "describe_global_replication_groups",
            "describe_replication_groups",
            "describe_reserved_cache_nodes",
            "describe_reserved_cache_nodes_offerings",
            "describe_service_updates",
            "describe_snapshots",
            "describe_update_actions",
            "describe_user_groups",
            "describe_users"
        ]
    },
    "elasticbeanstalk": {
        "List": [
            "list_available_solution_stacks",
            "list_platform_branches",
            "list_platform_versions",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_account_attributes",
            "describe_application_versions",
            "describe_applications",
            "describe_configuration_options",
            "describe_configuration_settings",
            "describe_environment_health",
            "describe_environment_managed_action_history",
            "describe_environment_managed_actions",
            "describe_environment_resources",
            "describe_environments",
            "describe_events",
            "describe_instances_health",
            "describe_platform_version"
        ]
    },
    "elastictranscoder": {
        "List": [
            "list_jobs_by_pipeline",
            "list_jobs_by_status",
            "list_pipelines",
            "list_presets"
        ],
        "Describe": []
    },
    "elb": {
        "List": [],
        "Describe": [
            "describe_account_limits",
            "describe_instance_health",
            "describe_load_balancer_attributes",
            "describe_load_balancer_policies",
            "describe_load_balancer_policy_types",
            "describe_load_balancers",
            "describe_tags"
        ]
    },
    "elbv2": {
        "List": [],
        "Describe": [
            "describe_account_limits",
            "describe_listener_certificates",
            "describe_listeners",
            "describe_load_balancer_attributes",
            "describe_load_balancers",
            "describe_rules",
            "describe_ssl_policies",
            "describe_tags",
            "describe_target_group_attributes",
            "describe_target_groups",
            "describe_target_health"
        ]
    },
    "emr": {
        "List": [
            "list_bootstrap_actions",
            "list_clusters",
            "list_instance_fleets",
            "list_instance_groups",
            "list_instances",
            "list_notebook_executions",
            "list_release_labels",
            "list_security_configurations",
            "list_steps",
            "list_studio_session_mappings",
            "list_studios"
        ],
        "Describe": [
            "describe_cluster",
            "describe_job_flows",
            "describe_notebook_execution",
            "describe_release_label",
            "describe_security_configuration",
            "describe_step",
            "describe_studio"
        ]
    },
    "emr-containers": {
        "List": [
            "list_job_runs",
            "list_managed_endpoints",
            "list_tags_for_resource",
            "list_virtual_clusters"
        ],
        "Describe": [
            "describe_job_run",
            "describe_managed_endpoint",
            "describe_virtual_cluster"
        ]
    },
    "es": {
        "List": [
            "list_domain_names",
            "list_domains_for_package",
            "list_elasticsearch_instance_types",
            "list_elasticsearch_versions",
            "list_packages_for_domain",
            "list_tags"
        ],
        "Describe": [
            "describe_domain_auto_tunes",
            "describe_elasticsearch_domain",
            "describe_elasticsearch_domain_config",
            "describe_elasticsearch_domains",
            "describe_elasticsearch_instance_type_limits",
            "describe_inbound_cross_cluster_search_connections",
            "describe_outbound_cross_cluster_search_connections",
            "describe_packages",
            "describe_reserved_elasticsearch_instance_offerings",
            "describe_reserved_elasticsearch_instances"
        ]
    },
    "events": {
        "List": [
            "list_api_destinations",
            "list_archives",
            "list_connections",
            "list_event_buses",
            "list_event_sources",
            "list_partner_event_source_accounts",
            "list_partner_event_sources",
            "list_replays",
            "list_rule_names_by_target",
            "list_rules",
            "list_tags_for_resource",
            "list_targets_by_rule"
        ],
        "Describe": [
            "describe_api_destination",
            "describe_archive",
            "describe_connection",
            "describe_event_bus",
            "describe_event_source",
            "describe_partner_event_source",
            "describe_replay",
            "describe_rule"
        ]
    },
    "finspace": {
        "List": [
            "list_environments",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "finspace-data": {
        "List": [],
        "Describe": []
    },
    "firehose": {
        "List": [
            "list_delivery_streams",
            "list_tags_for_delivery_stream"
        ],
        "Describe": [
            "describe_delivery_stream"
        ]
    },
    "fis": {
        "List": [
            "list_actions",
            "list_experiment_templates",
            "list_experiments",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "fms": {
        "List": [
            "list_apps_lists",
            "list_compliance_status",
            "list_member_accounts",
            "list_policies",
            "list_protocols_lists",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "forecast": {
        "List": [
            "list_dataset_groups",
            "list_dataset_import_jobs",
            "list_datasets",
            "list_forecast_export_jobs",
            "list_forecasts",
            "list_predictor_backtest_export_jobs",
            "list_predictors",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_dataset",
            "describe_dataset_group",
            "describe_dataset_import_job",
            "describe_forecast",
            "describe_forecast_export_job",
            "describe_predictor",
            "describe_predictor_backtest_export_job"
        ]
    },
    "forecastquery": {
        "List": [],
        "Describe": []
    },
    "frauddetector": {
        "List": [
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_detector",
            "describe_model_versions"
        ]
    },
    "fsx": {
        "List": [
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_backups",
            "describe_data_repository_tasks",
            "describe_file_system_aliases",
            "describe_file_systems",
            "describe_storage_virtual_machines",
            "describe_volumes"
        ]
    },
    "gamelift": {
        "List": [
            "list_aliases",
            "list_builds",
            "list_fleets",
            "list_game_server_groups",
            "list_game_servers",
            "list_scripts",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_alias",
            "describe_build",
            "describe_ec2_instance_limits",
            "describe_fleet_attributes",
            "describe_fleet_capacity",
            "describe_fleet_events",
            "describe_fleet_location_attributes",
            "describe_fleet_location_capacity",
            "describe_fleet_location_utilization",
            "describe_fleet_port_settings",
            "describe_fleet_utilization",
            "describe_game_server",
            "describe_game_server_group",
            "describe_game_server_instances",
            "describe_game_session_details",
            "describe_game_session_placement",
            "describe_game_session_queues",
            "describe_game_sessions",
            "describe_instances",
            "describe_matchmaking",
            "describe_matchmaking_configurations",
            "describe_matchmaking_rule_sets",
            "describe_player_sessions",
            "describe_runtime_configuration",
            "describe_scaling_policies",
            "describe_script",
            "describe_vpc_peering_authorizations",
            "describe_vpc_peering_connections"
        ]
    },
    "glacier": {
        "List": [
            "list_jobs",
            "list_multipart_uploads",
            "list_parts",
            "list_provisioned_capacity",
            "list_tags_for_vault",
            "list_vaults"
        ],
        "Describe": [
            "describe_job",
            "describe_vault"
        ]
    },
    "globalaccelerator": {
        "List": [
            "list_accelerators",
            "list_byoip_cidrs",
            "list_custom_routing_accelerators",
            "list_custom_routing_endpoint_groups",
            "list_custom_routing_listeners",
            "list_custom_routing_port_mappings",
            "list_custom_routing_port_mappings_by_destination",
            "list_endpoint_groups",
            "list_listeners",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_accelerator",
            "describe_accelerator_attributes",
            "describe_custom_routing_accelerator",
            "describe_custom_routing_accelerator_attributes",
            "describe_custom_routing_endpoint_group",
            "describe_custom_routing_listener",
            "describe_endpoint_group",
            "describe_listener"
        ]
    },
    "glue": {
        "List": [
            "list_blueprints",
            "list_crawlers",
            "list_dev_endpoints",
            "list_jobs",
            "list_ml_transforms",
            "list_registries",
            "list_schema_versions",
            "list_schemas",
            "list_triggers",
            "list_workflows"
        ],
        "Describe": []
    },
    "greengrass": {
        "List": [
            "list_bulk_deployment_detailed_reports",
            "list_bulk_deployments",
            "list_connector_definition_versions",
            "list_connector_definitions",
            "list_core_definition_versions",
            "list_core_definitions",
            "list_deployments",
            "list_device_definition_versions",
            "list_device_definitions",
            "list_function_definition_versions",
            "list_function_definitions",
            "list_group_certificate_authorities",
            "list_group_versions",
            "list_groups",
            "list_logger_definition_versions",
            "list_logger_definitions",
            "list_resource_definition_versions",
            "list_resource_definitions",
            "list_subscription_definition_versions",
            "list_subscription_definitions",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "greengrassv2": {
        "List": [
            "list_client_devices_associated_with_core_device",
            "list_component_versions",
            "list_components",
            "list_core_devices",
            "list_deployments",
            "list_effective_deployments",
            "list_installed_components",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_component"
        ]
    },
    "groundstation": {
        "List": [
            "list_configs",
            "list_contacts",
            "list_dataflow_endpoint_groups",
            "list_ground_stations",
            "list_mission_profiles",
            "list_satellites",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_contact"
        ]
    },
    "guardduty": {
        "List": [
            "list_detectors",
            "list_filters",
            "list_findings",
            "list_invitations",
            "list_ip_sets",
            "list_members",
            "list_organization_admin_accounts",
            "list_publishing_destinations",
            "list_tags_for_resource",
            "list_threat_intel_sets"
        ],
        "Describe": [
            "describe_organization_configuration",
            "describe_publishing_destination"
        ]
    },
    "health": {
        "List": [],
        "Describe": [
            "describe_affected_accounts_for_organization",
            "describe_affected_entities",
            "describe_affected_entities_for_organization",
            "describe_entity_aggregates",
            "describe_event_aggregates",
            "describe_event_details",
            "describe_event_details_for_organization",
            "describe_event_types",
            "describe_events",
            "describe_events_for_organization",
            "describe_health_service_status_for_organization"
        ]
    },
    "healthlake": {
        "List": [
            "list_fhir_datastores",
            "list_fhir_export_jobs",
            "list_fhir_import_jobs",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_fhir_datastore",
            "describe_fhir_export_job",
            "describe_fhir_import_job"
        ]
    },
    "honeycode": {
        "List": [
            "list_table_columns",
            "list_table_rows",
            "list_tables"
        ],
        "Describe": [
            "describe_table_data_import_job"
        ]
    },
    "identitystore": {
        "List": [
            "list_groups",
            "list_users"
        ],
        "Describe": [
            "describe_group",
            "describe_user"
        ]
    },
    "imagebuilder": {
        "List": [
            "list_component_build_versions",
            "list_components",
            "list_container_recipes",
            "list_distribution_configurations",
            "list_image_build_versions",
            "list_image_packages",
            "list_image_pipeline_images",
            "list_image_pipelines",
            "list_image_recipes",
            "list_images",
            "list_infrastructure_configurations",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "importexport": {
        "List": [
            "list_jobs"
        ],
        "Describe": []
    },
    "inspector": {
        "List": [
            "list_assessment_run_agents",
            "list_assessment_runs",
            "list_assessment_targets",
            "list_assessment_templates",
            "list_event_subscriptions",
            "list_exclusions",
            "list_findings",
            "list_rules_packages",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_assessment_runs",
            "describe_assessment_targets",
            "describe_assessment_templates",
            "describe_cross_account_access_role",
            "describe_exclusions",
            "describe_findings",
            "describe_resource_groups",
            "describe_rules_packages"
        ]
    },
    "iot": {
        "List": [
            "list_active_violations",
            "list_attached_policies",
            "list_audit_findings",
            "list_audit_mitigation_actions_executions",
            "list_audit_mitigation_actions_tasks",
            "list_audit_suppressions",
            "list_audit_tasks",
            "list_authorizers",
            "list_billing_groups",
            "list_ca_certificates",
            "list_certificates",
            "list_certificates_by_ca",
            "list_custom_metrics",
            "list_detect_mitigation_actions_executions",
            "list_detect_mitigation_actions_tasks",
            "list_dimensions",
            "list_domain_configurations",
            "list_fleet_metrics",
            "list_indices",
            "list_job_executions_for_job",
            "list_job_executions_for_thing",
            "list_job_templates",
            "list_jobs",
            "list_mitigation_actions",
            "list_ota_updates",
            "list_outgoing_certificates",
            "list_policies",
            "list_policy_principals",
            "list_policy_versions",
            "list_principal_policies",
            "list_principal_things",
            "list_provisioning_template_versions",
            "list_provisioning_templates",
            "list_role_aliases",
            "list_scheduled_audits",
            "list_security_profiles",
            "list_security_profiles_for_target",
            "list_streams",
            "list_tags_for_resource",
            "list_targets_for_policy",
            "list_targets_for_security_profile",
            "list_thing_groups",
            "list_thing_groups_for_thing",
            "list_thing_principals",
            "list_thing_registration_task_reports",
            "list_thing_registration_tasks",
            "list_thing_types",
            "list_things",
            "list_things_in_billing_group",
            "list_things_in_thing_group",
            "list_topic_rule_destinations",
            "list_topic_rules",
            "list_v2_logging_levels",
            "list_violation_events"
        ],
        "Describe": [
            "describe_account_audit_configuration",
            "describe_audit_finding",
            "describe_audit_mitigation_actions_task",
            "describe_audit_suppression",
            "describe_audit_task",
            "describe_authorizer",
            "describe_billing_group",
            "describe_ca_certificate",
            "describe_certificate",
            "describe_custom_metric",
            "describe_default_authorizer",
            "describe_detect_mitigation_actions_task",
            "describe_dimension",
            "describe_domain_configuration",
            "describe_endpoint",
            "describe_event_configurations",
            "describe_fleet_metric",
            "describe_index",
            "describe_job",
            "describe_job_execution",
            "describe_job_template",
            "describe_mitigation_action",
            "describe_provisioning_template",
            "describe_provisioning_template_version",
            "describe_role_alias",
            "describe_scheduled_audit",
            "describe_security_profile",
            "describe_stream",
            "describe_thing",
            "describe_thing_group",
            "describe_thing_registration_task",
            "describe_thing_type"
        ]
    },
    "iot-data": {
        "List": [
            "list_named_shadows_for_thing",
            "list_retained_messages"
        ],
        "Describe": []
    },
    "iot-jobs-data": {
        "List": [],
        "Describe": [
            "describe_job_execution"
        ]
    },
    "iot1click-devices": {
        "List": [
            "list_device_events",
            "list_devices",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_device"
        ]
    },
    "iot1click-projects": {
        "List": [
            "list_placements",
            "list_projects",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_placement",
            "describe_project"
        ]
    },
    "iotanalytics": {
        "List": [
            "list_channels",
            "list_dataset_contents",
            "list_datasets",
            "list_datastores",
            "list_pipelines",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_channel",
            "describe_dataset",
            "describe_datastore",
            "describe_logging_options",
            "describe_pipeline"
        ]
    },
    "iotdeviceadvisor": {
        "List": [
            "list_suite_definitions",
            "list_suite_runs",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "iotevents": {
        "List": [
            "list_alarm_model_versions",
            "list_alarm_models",
            "list_detector_model_versions",
            "list_detector_models",
            "list_input_routings",
            "list_inputs",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_alarm_model",
            "describe_detector_model",
            "describe_detector_model_analysis",
            "describe_input",
            "describe_logging_options"
        ]
    },
    "iotevents-data": {
        "List": [
            "list_alarms",
            "list_detectors"
        ],
        "Describe": [
            "describe_alarm",
            "describe_detector"
        ]
    },
    "iotfleethub": {
        "List": [
            "list_applications",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_application"
        ]
    },
    "iotsecuretunneling": {
        "List": [
            "list_tags_for_resource",
            "list_tunnels"
        ],
        "Describe": [
            "describe_tunnel"
        ]
    },
    "iotsitewise": {
        "List": [
            "list_access_policies",
            "list_asset_models",
            "list_asset_relationships",
            "list_assets",
            "list_associated_assets",
            "list_dashboards",
            "list_gateways",
            "list_portals",
            "list_project_assets",
            "list_projects",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_access_policy",
            "describe_asset",
            "describe_asset_model",
            "describe_asset_property",
            "describe_dashboard",
            "describe_default_encryption_configuration",
            "describe_gateway",
            "describe_gateway_capability_configuration",
            "describe_logging_options",
            "describe_portal",
            "describe_project",
            "describe_storage_configuration"
        ]
    },
    "iotthingsgraph": {
        "List": [
            "list_flow_execution_messages",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_namespace"
        ]
    },
    "iotwireless": {
        "List": [
            "list_destinations",
            "list_device_profiles",
            "list_partner_accounts",
            "list_service_profiles",
            "list_tags_for_resource",
            "list_wireless_devices",
            "list_wireless_gateway_task_definitions",
            "list_wireless_gateways"
        ],
        "Describe": []
    },
    "ivs": {
        "List": [
            "list_channels",
            "list_playback_key_pairs",
            "list_recording_configurations",
            "list_stream_keys",
            "list_streams",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "kafka": {
        "List": [
            "list_cluster_operations",
            "list_clusters",
            "list_configuration_revisions",
            "list_configurations",
            "list_kafka_versions",
            "list_nodes",
            "list_scram_secrets",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_cluster",
            "describe_cluster_operation",
            "describe_configuration",
            "describe_configuration_revision"
        ]
    },
    "kendra": {
        "List": [
            "list_data_source_sync_jobs",
            "list_data_sources",
            "list_faqs",
            "list_groups_older_than_ordering_id",
            "list_indices",
            "list_query_suggestions_block_lists",
            "list_tags_for_resource",
            "list_thesauri"
        ],
        "Describe": [
            "describe_data_source",
            "describe_faq",
            "describe_index",
            "describe_principal_mapping",
            "describe_query_suggestions_block_list",
            "describe_query_suggestions_config",
            "describe_thesaurus"
        ]
    },
    "kinesis": {
        "List": [
            "list_shards",
            "list_stream_consumers",
            "list_streams",
            "list_tags_for_stream"
        ],
        "Describe": [
            "describe_limits",
            "describe_stream",
            "describe_stream_consumer",
            "describe_stream_summary"
        ]
    },
    "kinesis-video-archived-media": {
        "List": [
            "list_fragments"
        ],
        "Describe": []
    },
    "kinesis-video-media": {
        "List": [],
        "Describe": []
    },
    "kinesis-video-signaling": {
        "List": [],
        "Describe": []
    },
    "kinesisanalytics": {
        "List": [
            "list_applications",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_application"
        ]
    },
    "kinesisanalyticsv2": {
        "List": [
            "list_application_snapshots",
            "list_application_versions",
            "list_applications",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_application",
            "describe_application_snapshot",
            "describe_application_version"
        ]
    },
    "kinesisvideo": {
        "List": [
            "list_signaling_channels",
            "list_streams",
            "list_tags_for_resource",
            "list_tags_for_stream"
        ],
        "Describe": [
            "describe_signaling_channel",
            "describe_stream"
        ]
    },
    "kms": {
        "List": [
            "list_aliases",
            "list_grants",
            "list_key_policies",
            "list_keys",
            "list_resource_tags",
            "list_retirable_grants"
        ],
        "Describe": [
            "describe_custom_key_stores",
            "describe_key"
        ]
    },
    "lakeformation": {
        "List": [
            "list_lf_tags",
            "list_permissions",
            "list_resources"
        ],
        "Describe": [
            "describe_resource"
        ]
    },
    "lex-models": {
        "List": [
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "lex-runtime": {
        "List": [],
        "Describe": []
    },
    "lexv2-models": {
        "List": [
            "list_aggregated_utterances",
            "list_bot_aliases",
            "list_bot_locales",
            "list_bot_versions",
            "list_bots",
            "list_built_in_intents",
            "list_built_in_slot_types",
            "list_exports",
            "list_imports",
            "list_intents",
            "list_slot_types",
            "list_slots",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_bot",
            "describe_bot_alias",
            "describe_bot_locale",
            "describe_bot_version",
            "describe_export",
            "describe_import",
            "describe_intent",
            "describe_resource_policy",
            "describe_slot",
            "describe_slot_type"
        ]
    },
    "lexv2-runtime": {
        "List": [],
        "Describe": []
    },
    "license-manager": {
        "List": [
            "list_associations_for_license_configuration",
            "list_distributed_grants",
            "list_failures_for_license_configuration_operations",
            "list_license_configurations",
            "list_license_conversion_tasks",
            "list_license_manager_report_generators",
            "list_license_specifications_for_resource",
            "list_license_versions",
            "list_licenses",
            "list_received_grants",
            "list_received_licenses",
            "list_resource_inventory",
            "list_tags_for_resource",
            "list_tokens",
            "list_usage_for_license_configuration"
        ],
        "Describe": []
    },
    "lightsail": {
        "List": [],
        "Describe": []
    },
    "location": {
        "List": [
            "list_device_positions",
            "list_geofence_collections",
            "list_geofences",
            "list_maps",
            "list_place_indexes",
            "list_route_calculators",
            "list_tags_for_resource",
            "list_tracker_consumers",
            "list_trackers"
        ],
        "Describe": [
            "describe_geofence_collection",
            "describe_map",
            "describe_place_index",
            "describe_route_calculator",
            "describe_tracker"
        ]
    },
    "logs": {
        "List": [
            "list_tags_log_group"
        ],
        "Describe": [
            "describe_destinations",
            "describe_export_tasks",
            "describe_log_groups",
            "describe_log_streams",
            "describe_metric_filters",
            "describe_queries",
            "describe_query_definitions",
            "describe_resource_policies",
            "describe_subscription_filters"
        ]
    },
    "lookoutequipment": {
        "List": [
            "list_data_ingestion_jobs",
            "list_datasets",
            "list_inference_executions",
            "list_inference_schedulers",
            "list_models",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_data_ingestion_job",
            "describe_dataset",
            "describe_inference_scheduler",
            "describe_model"
        ]
    },
    "lookoutmetrics": {
        "List": [
            "list_alerts",
            "list_anomaly_detectors",
            "list_anomaly_group_summaries",
            "list_anomaly_group_time_series",
            "list_metric_sets",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_alert",
            "describe_anomaly_detection_executions",
            "describe_anomaly_detector",
            "describe_metric_set"
        ]
    },
    "lookoutvision": {
        "List": [
            "list_dataset_entries",
            "list_models",
            "list_projects",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_dataset",
            "describe_model",
            "describe_project"
        ]
    },
    "machinelearning": {
        "List": [],
        "Describe": [
            "describe_batch_predictions",
            "describe_data_sources",
            "describe_evaluations",
            "describe_ml_models",
            "describe_tags"
        ]
    },
    "macie": {
        "List": [
            "list_member_accounts",
            "list_s3_resources"
        ],
        "Describe": []
    },
    "macie2": {
        "List": [
            "list_classification_jobs",
            "list_custom_data_identifiers",
            "list_findings",
            "list_findings_filters",
            "list_invitations",
            "list_managed_data_identifiers",
            "list_members",
            "list_organization_admin_accounts",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_buckets",
            "describe_classification_job",
            "describe_organization_configuration"
        ]
    },
    "managedblockchain": {
        "List": [
            "list_invitations",
            "list_members",
            "list_networks",
            "list_nodes",
            "list_proposal_votes",
            "list_proposals",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "marketplace-catalog": {
        "List": [
            "list_change_sets",
            "list_entities"
        ],
        "Describe": [
            "describe_change_set",
            "describe_entity"
        ]
    },
    "marketplace-entitlement": {
        "List": [],
        "Describe": []
    },
    "marketplacecommerceanalytics": {
        "List": [],
        "Describe": []
    },
    "mediaconnect": {
        "List": [
            "list_entitlements",
            "list_flows",
            "list_offerings",
            "list_reservations",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_flow",
            "describe_offering",
            "describe_reservation"
        ]
    },
    "mediaconvert": {
        "List": [
            "list_job_templates",
            "list_jobs",
            "list_presets",
            "list_queues",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_endpoints"
        ]
    },
    "medialive": {
        "List": [
            "list_channels",
            "list_input_device_transfers",
            "list_input_devices",
            "list_input_security_groups",
            "list_inputs",
            "list_multiplex_programs",
            "list_multiplexes",
            "list_offerings",
            "list_reservations",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_channel",
            "describe_input",
            "describe_input_device",
            "describe_input_device_thumbnail",
            "describe_input_security_group",
            "describe_multiplex",
            "describe_multiplex_program",
            "describe_offering",
            "describe_reservation",
            "describe_schedule"
        ]
    },
    "mediapackage": {
        "List": [
            "list_channels",
            "list_harvest_jobs",
            "list_origin_endpoints",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_channel",
            "describe_harvest_job",
            "describe_origin_endpoint"
        ]
    },
    "mediapackage-vod": {
        "List": [
            "list_assets",
            "list_packaging_configurations",
            "list_packaging_groups",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_asset",
            "describe_packaging_configuration",
            "describe_packaging_group"
        ]
    },
    "mediastore": {
        "List": [
            "list_containers",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_container"
        ]
    },
    "mediastore-data": {
        "List": [
            "list_items"
        ],
        "Describe": [
            "describe_object"
        ]
    },
    "mediatailor": {
        "List": [
            "list_alerts",
            "list_channels",
            "list_playback_configurations",
            "list_prefetch_schedules",
            "list_source_locations",
            "list_tags_for_resource",
            "list_vod_sources"
        ],
        "Describe": [
            "describe_channel",
            "describe_program",
            "describe_source_location",
            "describe_vod_source"
        ]
    },
    "meteringmarketplace": {
        "List": [],
        "Describe": []
    },
    "mgh": {
        "List": [
            "list_application_states",
            "list_created_artifacts",
            "list_discovered_resources",
            "list_migration_tasks",
            "list_progress_update_streams"
        ],
        "Describe": [
            "describe_application_state",
            "describe_migration_task"
        ]
    },
    "mgn": {
        "List": [
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_job_log_items",
            "describe_jobs",
            "describe_replication_configuration_templates",
            "describe_source_servers"
        ]
    },
    "migrationhub-config": {
        "List": [],
        "Describe": [
            "describe_home_region_controls"
        ]
    },
    "mobile": {
        "List": [
            "list_bundles",
            "list_projects"
        ],
        "Describe": [
            "describe_bundle",
            "describe_project"
        ]
    },
    "mq": {
        "List": [
            "list_brokers",
            "list_configuration_revisions",
            "list_configurations",
            "list_tags",
            "list_users"
        ],
        "Describe": [
            "describe_broker",
            "describe_broker_engine_types",
            "describe_broker_instance_options",
            "describe_configuration",
            "describe_configuration_revision",
            "describe_user"
        ]
    },
    "mturk": {
        "List": [
            "list_assignments_for_hit",
            "list_bonus_payments",
            "list_hits",
            "list_hits_for_qualification_type",
            "list_qualification_requests",
            "list_qualification_types",
            "list_review_policy_results_for_hit",
            "list_reviewable_hits",
            "list_worker_blocks",
            "list_workers_with_qualification_type"
        ],
        "Describe": []
    },
    "mwaa": {
        "List": [
            "list_environments",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "neptune": {
        "List": [
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_db_cluster_endpoints",
            "describe_db_cluster_parameter_groups",
            "describe_db_cluster_parameters",
            "describe_db_cluster_snapshot_attributes",
            "describe_db_cluster_snapshots",
            "describe_db_clusters",
            "describe_db_engine_versions",
            "describe_db_instances",
            "describe_db_parameter_groups",
            "describe_db_parameters",
            "describe_db_subnet_groups",
            "describe_engine_default_cluster_parameters",
            "describe_engine_default_parameters",
            "describe_event_categories",
            "describe_event_subscriptions",
            "describe_events",
            "describe_orderable_db_instance_options",
            "describe_pending_maintenance_actions",
            "describe_valid_db_instance_modifications"
        ]
    },
    "network-firewall": {
        "List": [
            "list_firewall_policies",
            "list_firewalls",
            "list_rule_groups",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_firewall",
            "describe_firewall_policy",
            "describe_logging_configuration",
            "describe_resource_policy",
            "describe_rule_group"
        ]
    },
    "networkmanager": {
        "List": [
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_global_networks"
        ]
    },
    "nimble": {
        "List": [
            "list_eula_acceptances",
            "list_eulas",
            "list_launch_profile_members",
            "list_launch_profiles",
            "list_streaming_images",
            "list_streaming_sessions",
            "list_studio_components",
            "list_studio_members",
            "list_studios",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "opsworks": {
        "List": [
            "list_tags"
        ],
        "Describe": [
            "describe_agent_versions",
            "describe_apps",
            "describe_commands",
            "describe_deployments",
            "describe_ecs_clusters",
            "describe_elastic_ips",
            "describe_elastic_load_balancers",
            "describe_instances",
            "describe_layers",
            "describe_load_based_auto_scaling",
            "describe_my_user_profile",
            "describe_operating_systems",
            "describe_permissions",
            "describe_raid_arrays",
            "describe_rds_db_instances",
            "describe_service_errors",
            "describe_stack_provisioning_parameters",
            "describe_stack_summary",
            "describe_stacks",
            "describe_time_based_auto_scaling",
            "describe_user_profiles",
            "describe_volumes"
        ]
    },
    "opsworkscm": {
        "List": [
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_account_attributes",
            "describe_backups",
            "describe_events",
            "describe_node_association_status",
            "describe_servers"
        ]
    },
    "organizations": {
        "List": [
            "list_accounts",
            "list_accounts_for_parent",
            "list_aws_service_access_for_organization",
            "list_children",
            "list_create_account_status",
            "list_delegated_administrators",
            "list_delegated_services_for_account",
            "list_handshakes_for_account",
            "list_handshakes_for_organization",
            "list_organizational_units_for_parent",
            "list_parents",
            "list_policies",
            "list_policies_for_target",
            "list_roots",
            "list_tags_for_resource",
            "list_targets_for_policy"
        ],
        "Describe": [
            "describe_account",
            "describe_create_account_status",
            "describe_effective_policy",
            "describe_handshake",
            "describe_organization",
            "describe_organizational_unit",
            "describe_policy"
        ]
    },
    "outposts": {
        "List": [
            "list_outposts",
            "list_sites",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "personalize": {
        "List": [
            "list_batch_inference_jobs",
            "list_campaigns",
            "list_dataset_export_jobs",
            "list_dataset_groups",
            "list_dataset_import_jobs",
            "list_datasets",
            "list_event_trackers",
            "list_filters",
            "list_recipes",
            "list_schemas",
            "list_solution_versions",
            "list_solutions"
        ],
        "Describe": [
            "describe_algorithm",
            "describe_batch_inference_job",
            "describe_campaign",
            "describe_dataset",
            "describe_dataset_export_job",
            "describe_dataset_group",
            "describe_dataset_import_job",
            "describe_event_tracker",
            "describe_feature_transformation",
            "describe_filter",
            "describe_recipe",
            "describe_schema",
            "describe_solution",
            "describe_solution_version"
        ]
    },
    "personalize-events": {
        "List": [],
        "Describe": []
    },
    "personalize-runtime": {
        "List": [],
        "Describe": []
    },
    "pi": {
        "List": [],
        "Describe": [
            "describe_dimension_keys"
        ]
    },
    "pinpoint": {
        "List": [
            "list_journeys",
            "list_tags_for_resource",
            "list_template_versions",
            "list_templates"
        ],
        "Describe": []
    },
    "pinpoint-email": {
        "List": [
            "list_configuration_sets",
            "list_dedicated_ip_pools",
            "list_deliverability_test_reports",
            "list_domain_deliverability_campaigns",
            "list_email_identities",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "pinpoint-sms-voice": {
        "List": [],
        "Describe": []
    },
    "polly": {
        "List": [
            "list_lexicons",
            "list_speech_synthesis_tasks"
        ],
        "Describe": [
            "describe_voices"
        ]
    },
    "pricing": {
        "List": [],
        "Describe": [
            "describe_services"
        ]
    },
    "qldb": {
        "List": [
            "list_journal_kinesis_streams_for_ledger",
            "list_journal_s3_exports",
            "list_journal_s3_exports_for_ledger",
            "list_ledgers",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_journal_kinesis_stream",
            "describe_journal_s3_export",
            "describe_ledger"
        ]
    },
    "qldb-session": {
        "List": [],
        "Describe": []
    },
    "quicksight": {
        "List": [
            "list_analyses",
            "list_dashboard_versions",
            "list_dashboards",
            "list_data_sets",
            "list_data_sources",
            "list_folder_members",
            "list_folders",
            "list_group_memberships",
            "list_groups",
            "list_iam_policy_assignments",
            "list_iam_policy_assignments_for_user",
            "list_ingestions",
            "list_namespaces",
            "list_tags_for_resource",
            "list_template_aliases",
            "list_template_versions",
            "list_templates",
            "list_theme_aliases",
            "list_theme_versions",
            "list_themes",
            "list_user_groups",
            "list_users"
        ],
        "Describe": [
            "describe_account_customization",
            "describe_account_settings",
            "describe_analysis",
            "describe_analysis_permissions",
            "describe_dashboard",
            "describe_dashboard_permissions",
            "describe_data_set",
            "describe_data_set_permissions",
            "describe_data_source",
            "describe_data_source_permissions",
            "describe_folder",
            "describe_folder_permissions",
            "describe_folder_resolved_permissions",
            "describe_group",
            "describe_iam_policy_assignment",
            "describe_ingestion",
            "describe_ip_restriction",
            "describe_namespace",
            "describe_template",
            "describe_template_alias",
            "describe_template_permissions",
            "describe_theme",
            "describe_theme_alias",
            "describe_theme_permissions",
            "describe_user"
        ]
    },
    "ram": {
        "List": [
            "list_pending_invitation_resources",
            "list_permissions",
            "list_principals",
            "list_resource_share_permissions",
            "list_resource_types",
            "list_resources"
        ],
        "Describe": []
    },
    "rds": {
        "List": [
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_account_attributes",
            "describe_certificates",
            "describe_custom_availability_zones",
            "describe_db_cluster_backtracks",
            "describe_db_cluster_endpoints",
            "describe_db_cluster_parameter_groups",
            "describe_db_cluster_parameters",
            "describe_db_cluster_snapshot_attributes",
            "describe_db_cluster_snapshots",
            "describe_db_clusters",
            "describe_db_engine_versions",
            "describe_db_instance_automated_backups",
            "describe_db_instances",
            "describe_db_log_files",
            "describe_db_parameter_groups",
            "describe_db_parameters",
            "describe_db_proxies",
            "describe_db_proxy_endpoints",
            "describe_db_proxy_target_groups",
            "describe_db_proxy_targets",
            "describe_db_security_groups",
            "describe_db_snapshot_attributes",
            "describe_db_snapshots",
            "describe_db_subnet_groups",
            "describe_engine_default_cluster_parameters",
            "describe_engine_default_parameters",
            "describe_event_categories",
            "describe_event_subscriptions",
            "describe_events",
            "describe_export_tasks",
            "describe_global_clusters",
            "describe_installation_media",
            "describe_option_group_options",
            "describe_option_groups",
            "describe_orderable_db_instance_options",
            "describe_pending_maintenance_actions",
            "describe_reserved_db_instances",
            "describe_reserved_db_instances_offerings",
            "describe_source_regions",
            "describe_valid_db_instance_modifications"
        ]
    },
    "rds-data": {
        "List": [],
        "Describe": []
    },
    "redshift": {
        "List": [],
        "Describe": [
            "describe_account_attributes",
            "describe_authentication_profiles",
            "describe_cluster_db_revisions",
            "describe_cluster_parameter_groups",
            "describe_cluster_parameters",
            "describe_cluster_security_groups",
            "describe_cluster_snapshots",
            "describe_cluster_subnet_groups",
            "describe_cluster_tracks",
            "describe_cluster_versions",
            "describe_clusters",
            "describe_data_shares",
            "describe_data_shares_for_consumer",
            "describe_data_shares_for_producer",
            "describe_default_cluster_parameters",
            "describe_endpoint_access",
            "describe_endpoint_authorization",
            "describe_event_categories",
            "describe_event_subscriptions",
            "describe_events",
            "describe_hsm_client_certificates",
            "describe_hsm_configurations",
            "describe_logging_status",
            "describe_node_configuration_options",
            "describe_orderable_cluster_options",
            "describe_partners",
            "describe_reserved_node_offerings",
            "describe_reserved_nodes",
            "describe_resize",
            "describe_scheduled_actions",
            "describe_snapshot_copy_grants",
            "describe_snapshot_schedules",
            "describe_storage",
            "describe_table_restore_status",
            "describe_tags",
            "describe_usage_limits"
        ]
    },
    "redshift-data": {
        "List": [
            "list_databases",
            "list_schemas",
            "list_statements",
            "list_tables"
        ],
        "Describe": [
            "describe_statement",
            "describe_table"
        ]
    },
    "rekognition": {
        "List": [
            "list_collections",
            "list_faces",
            "list_stream_processors",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_collection",
            "describe_project_versions",
            "describe_projects",
            "describe_stream_processor"
        ]
    },
    "resource-groups": {
        "List": [
            "list_group_resources",
            "list_groups"
        ],
        "Describe": []
    },
    "resourcegroupstaggingapi": {
        "List": [],
        "Describe": [
            "describe_report_creation"
        ]
    },
    "robomaker": {
        "List": [
            "list_deployment_jobs",
            "list_fleets",
            "list_robot_applications",
            "list_robots",
            "list_simulation_applications",
            "list_simulation_job_batches",
            "list_simulation_jobs",
            "list_tags_for_resource",
            "list_world_export_jobs",
            "list_world_generation_jobs",
            "list_world_templates",
            "list_worlds"
        ],
        "Describe": [
            "describe_deployment_job",
            "describe_fleet",
            "describe_robot",
            "describe_robot_application",
            "describe_simulation_application",
            "describe_simulation_job",
            "describe_simulation_job_batch",
            "describe_world",
            "describe_world_export_job",
            "describe_world_generation_job",
            "describe_world_template"
        ]
    },
    "route53": {
        "List": [
            "list_geo_locations",
            "list_health_checks",
            "list_hosted_zones",
            "list_hosted_zones_by_name",
            "list_hosted_zones_by_vpc",
            "list_query_logging_configs",
            "list_resource_record_sets",
            "list_reusable_delegation_sets",
            "list_tags_for_resource",
            "list_tags_for_resources",
            "list_traffic_policies",
            "list_traffic_policy_instances",
            "list_traffic_policy_instances_by_hosted_zone",
            "list_traffic_policy_instances_by_policy",
            "list_traffic_policy_versions",
            "list_vpc_association_authorizations"
        ],
        "Describe": []
    },
    "route53domains": {
        "List": [
            "list_domains",
            "list_operations",
            "list_tags_for_domain"
        ],
        "Describe": []
    },
    "route53resolver": {
        "List": [
            "list_firewall_configs",
            "list_firewall_domain_lists",
            "list_firewall_domains",
            "list_firewall_rule_group_associations",
            "list_firewall_rule_groups",
            "list_firewall_rules",
            "list_resolver_dnssec_configs",
            "list_resolver_endpoint_ip_addresses",
            "list_resolver_endpoints",
            "list_resolver_query_log_config_associations",
            "list_resolver_query_log_configs",
            "list_resolver_rule_associations",
            "list_resolver_rules",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "s3control": {
        "List": [
            "list_access_points",
            "list_access_points_for_object_lambda",
            "list_jobs",
            "list_multi_region_access_points",
            "list_regional_buckets",
            "list_storage_lens_configurations"
        ],
        "Describe": [
            "describe_job",
            "describe_multi_region_access_point_operation"
        ]
    },
    "s3outposts": {
        "List": [
            "list_endpoints"
        ],
        "Describe": []
    },
    "sagemaker": {
        "List": [
            "list_actions",
            "list_algorithms",
            "list_app_image_configs",
            "list_apps",
            "list_artifacts",
            "list_associations",
            "list_auto_ml_jobs",
            "list_candidates_for_auto_ml_job",
            "list_code_repositories",
            "list_compilation_jobs",
            "list_contexts",
            "list_data_quality_job_definitions",
            "list_device_fleets",
            "list_devices",
            "list_domains",
            "list_edge_packaging_jobs",
            "list_endpoint_configs",
            "list_endpoints",
            "list_experiments",
            "list_feature_groups",
            "list_flow_definitions",
            "list_human_task_uis",
            "list_hyper_parameter_tuning_jobs",
            "list_image_versions",
            "list_images",
            "list_labeling_jobs",
            "list_labeling_jobs_for_workteam",
            "list_model_bias_job_definitions",
            "list_model_explainability_job_definitions",
            "list_model_package_groups",
            "list_model_packages",
            "list_model_quality_job_definitions",
            "list_models",
            "list_monitoring_executions",
            "list_monitoring_schedules",
            "list_notebook_instance_lifecycle_configs",
            "list_notebook_instances",
            "list_pipeline_execution_steps",
            "list_pipeline_executions",
            "list_pipeline_parameters_for_execution",
            "list_pipelines",
            "list_processing_jobs",
            "list_projects",
            "list_studio_lifecycle_configs",
            "list_subscribed_workteams",
            "list_tags",
            "list_training_jobs",
            "list_training_jobs_for_hyper_parameter_tuning_job",
            "list_transform_jobs",
            "list_trial_components",
            "list_trials",
            "list_user_profiles",
            "list_workforces",
            "list_workteams"
        ],
        "Describe": [
            "describe_action",
            "describe_algorithm",
            "describe_app",
            "describe_app_image_config",
            "describe_artifact",
            "describe_auto_ml_job",
            "describe_code_repository",
            "describe_compilation_job",
            "describe_context",
            "describe_data_quality_job_definition",
            "describe_device",
            "describe_device_fleet",
            "describe_domain",
            "describe_edge_packaging_job",
            "describe_endpoint",
            "describe_endpoint_config",
            "describe_experiment",
            "describe_feature_group",
            "describe_flow_definition",
            "describe_human_task_ui",
            "describe_hyper_parameter_tuning_job",
            "describe_image",
            "describe_image_version",
            "describe_labeling_job",
            "describe_model",
            "describe_model_bias_job_definition",
            "describe_model_explainability_job_definition",
            "describe_model_package",
            "describe_model_package_group",
            "describe_model_quality_job_definition",
            "describe_monitoring_schedule",
            "describe_notebook_instance",
            "describe_notebook_instance_lifecycle_config",
            "describe_pipeline",
            "describe_pipeline_definition_for_execution",
            "describe_pipeline_execution",
            "describe_processing_job",
            "describe_project",
            "describe_studio_lifecycle_config",
            "describe_subscribed_workteam",
            "describe_training_job",
            "describe_transform_job",
            "describe_trial",
            "describe_trial_component",
            "describe_user_profile",
            "describe_workforce",
            "describe_workteam"
        ]
    },
    "sagemaker-a2i-runtime": {
        "List": [
            "list_human_loops"
        ],
        "Describe": [
            "describe_human_loop"
        ]
    },
    "sagemaker-edge": {
        "List": [],
        "Describe": []
    },
    "sagemaker-featurestore-runtime": {
        "List": [],
        "Describe": []
    },
    "sagemaker-runtime": {
        "List": [],
        "Describe": []
    },
    "savingsplans": {
        "List": [
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_savings_plan_rates",
            "describe_savings_plans",
            "describe_savings_plans_offering_rates",
            "describe_savings_plans_offerings"
        ]
    },
    "schemas": {
        "List": [
            "list_discoverers",
            "list_registries",
            "list_schema_versions",
            "list_schemas",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_code_binding",
            "describe_discoverer",
            "describe_registry",
            "describe_schema"
        ]
    },
    "sdb": {
        "List": [
            "list_domains"
        ],
        "Describe": []
    },
    "secretsmanager": {
        "List": [
            "list_secret_version_ids",
            "list_secrets"
        ],
        "Describe": [
            "describe_secret"
        ]
    },
    "securityhub": {
        "List": [
            "list_enabled_products_for_import",
            "list_invitations",
            "list_members",
            "list_organization_admin_accounts",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_action_targets",
            "describe_hub",
            "describe_organization_configuration",
            "describe_products",
            "describe_standards",
            "describe_standards_controls"
        ]
    },
    "serverlessrepo": {
        "List": [
            "list_application_dependencies",
            "list_application_versions",
            "list_applications"
        ],
        "Describe": []
    },
    "service-quotas": {
        "List": [
            "list_aws_default_service_quotas",
            "list_requested_service_quota_change_history",
            "list_requested_service_quota_change_history_by_quota",
            "list_service_quota_increase_requests_in_template",
            "list_service_quotas",
            "list_services",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "servicecatalog": {
        "List": [
            "list_accepted_portfolio_shares",
            "list_budgets_for_resource",
            "list_constraints_for_portfolio",
            "list_launch_paths",
            "list_organization_portfolio_access",
            "list_portfolio_access",
            "list_portfolios",
            "list_portfolios_for_product",
            "list_principals_for_portfolio",
            "list_provisioned_product_plans",
            "list_provisioning_artifacts",
            "list_provisioning_artifacts_for_service_action",
            "list_record_history",
            "list_resources_for_tag_option",
            "list_service_actions",
            "list_service_actions_for_provisioning_artifact",
            "list_stack_instances_for_provisioned_product",
            "list_tag_options"
        ],
        "Describe": [
            "describe_constraint",
            "describe_copy_product_status",
            "describe_portfolio",
            "describe_portfolio_share_status",
            "describe_portfolio_shares",
            "describe_product",
            "describe_product_as_admin",
            "describe_product_view",
            "describe_provisioned_product",
            "describe_provisioned_product_plan",
            "describe_provisioning_artifact",
            "describe_provisioning_parameters",
            "describe_record",
            "describe_service_action",
            "describe_service_action_execution_parameters",
            "describe_tag_option"
        ]
    },
    "servicecatalog-appregistry": {
        "List": [
            "list_applications",
            "list_associated_attribute_groups",
            "list_associated_resources",
            "list_attribute_groups",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "servicediscovery": {
        "List": [
            "list_instances",
            "list_namespaces",
            "list_operations",
            "list_services",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "ses": {
        "List": [
            "list_configuration_sets",
            "list_custom_verification_email_templates",
            "list_identities",
            "list_identity_policies",
            "list_receipt_filters",
            "list_receipt_rule_sets",
            "list_templates",
            "list_verified_email_addresses"
        ],
        "Describe": [
            "describe_active_receipt_rule_set",
            "describe_configuration_set",
            "describe_receipt_rule",
            "describe_receipt_rule_set"
        ]
    },
    "sesv2": {
        "List": [
            "list_configuration_sets",
            "list_contact_lists",
            "list_contacts",
            "list_custom_verification_email_templates",
            "list_dedicated_ip_pools",
            "list_deliverability_test_reports",
            "list_domain_deliverability_campaigns",
            "list_email_identities",
            "list_email_templates",
            "list_import_jobs",
            "list_suppressed_destinations",
            "list_tags_for_resource"
        ],
        "Describe": []
    },
    "shield": {
        "List": [
            "list_attacks",
            "list_protection_groups",
            "list_protections",
            "list_resources_in_protection_group",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_attack",
            "describe_attack_statistics",
            "describe_drt_access",
            "describe_emergency_contact_settings",
            "describe_protection",
            "describe_protection_group",
            "describe_subscription"
        ]
    },
    "signer": {
        "List": [
            "list_profile_permissions",
            "list_signing_jobs",
            "list_signing_platforms",
            "list_signing_profiles",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_signing_job"
        ]
    },
    "sms": {
        "List": [
            "list_apps"
        ],
        "Describe": []
    },
    "sms-voice": {
        "List": [
            "list_configuration_sets"
        ],
        "Describe": []
    },
    "snowball": {
        "List": [
            "list_cluster_jobs",
            "list_clusters",
            "list_compatible_images",
            "list_jobs",
            "list_long_term_pricing"
        ],
        "Describe": [
            "describe_address",
            "describe_addresses",
            "describe_cluster",
            "describe_job",
            "describe_return_shipping_label"
        ]
    },
    "sns": {
        "List": [
            "list_endpoints_by_platform_application",
            "list_origination_numbers",
            "list_phone_numbers_opted_out",
            "list_platform_applications",
            "list_sms_sandbox_phone_numbers",
            "list_subscriptions",
            "list_subscriptions_by_topic",
            "list_tags_for_resource",
            "list_topics"
        ],
        "Describe": []
    },
    "sqs": {
        "List": [
            "list_dead_letter_source_queues",
            "list_queue_tags",
            "list_queues"
        ],
        "Describe": []
    },
    "ssm": {
        "List": [
            "list_association_versions",
            "list_associations",
            "list_command_invocations",
            "list_commands",
            "list_compliance_items",
            "list_compliance_summaries",
            "list_document_metadata_history",
            "list_document_versions",
            "list_documents",
            "list_inventory_entries",
            "list_ops_item_events",
            "list_ops_item_related_items",
            "list_ops_metadata",
            "list_resource_compliance_summaries",
            "list_resource_data_sync",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_activations",
            "describe_association",
            "describe_association_execution_targets",
            "describe_association_executions",
            "describe_automation_executions",
            "describe_automation_step_executions",
            "describe_available_patches",
            "describe_document",
            "describe_document_permission",
            "describe_effective_instance_associations",
            "describe_effective_patches_for_patch_baseline",
            "describe_instance_associations_status",
            "describe_instance_information",
            "describe_instance_patch_states",
            "describe_instance_patch_states_for_patch_group",
            "describe_instance_patches",
            "describe_inventory_deletions",
            "describe_maintenance_window_execution_task_invocations",
            "describe_maintenance_window_execution_tasks",
            "describe_maintenance_window_executions",
            "describe_maintenance_window_schedule",
            "describe_maintenance_window_targets",
            "describe_maintenance_window_tasks",
            "describe_maintenance_windows",
            "describe_maintenance_windows_for_target",
            "describe_ops_items",
            "describe_parameters",
            "describe_patch_baselines",
            "describe_patch_group_state",
            "describe_patch_groups",
            "describe_patch_properties",
            "describe_sessions"
        ]
    },
    "ssm-contacts": {
        "List": [
            "list_contact_channels",
            "list_contacts",
            "list_engagements",
            "list_page_receipts",
            "list_pages_by_contact",
            "list_pages_by_engagement",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_engagement",
            "describe_page"
        ]
    },
    "ssm-incidents": {
        "List": [
            "list_incident_records",
            "list_related_items",
            "list_replication_sets",
            "list_response_plans",
            "list_tags_for_resource",
            "list_timeline_events"
        ],
        "Describe": []
    },
    "sso": {
        "List": [
            "list_account_roles",
            "list_accounts"
        ],
        "Describe": []
    },
    "sso-admin": {
        "List": [
            "list_account_assignment_creation_status",
            "list_account_assignment_deletion_status",
            "list_account_assignments",
            "list_accounts_for_provisioned_permission_set",
            "list_instances",
            "list_managed_policies_in_permission_set",
            "list_permission_set_provisioning_status",
            "list_permission_sets",
            "list_permission_sets_provisioned_to_account",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_account_assignment_creation_status",
            "describe_account_assignment_deletion_status",
            "describe_instance_access_control_attribute_configuration",
            "describe_permission_set",
            "describe_permission_set_provisioning_status"
        ]
    },
    "sso-oidc": {
        "List": [],
        "Describe": []
    },
    "stepfunctions": {
        "List": [
            "list_activities",
            "list_executions",
            "list_state_machines",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_activity",
            "describe_execution",
            "describe_state_machine",
            "describe_state_machine_for_execution"
        ]
    },
    "storagegateway": {
        "List": [
            "list_automatic_tape_creation_policies",
            "list_file_shares",
            "list_file_system_associations",
            "list_gateways",
            "list_local_disks",
            "list_tags_for_resource",
            "list_tape_pools",
            "list_tapes",
            "list_volume_initiators",
            "list_volume_recovery_points",
            "list_volumes"
        ],
        "Describe": [
            "describe_availability_monitor_test",
            "describe_bandwidth_rate_limit",
            "describe_bandwidth_rate_limit_schedule",
            "describe_cache",
            "describe_cached_iscsi_volumes",
            "describe_chap_credentials",
            "describe_file_system_associations",
            "describe_gateway_information",
            "describe_maintenance_start_time",
            "describe_nfs_file_shares",
            "describe_smb_file_shares",
            "describe_smb_settings",
            "describe_snapshot_schedule",
            "describe_stored_iscsi_volumes",
            "describe_tape_archives",
            "describe_tape_recovery_points",
            "describe_tapes",
            "describe_upload_buffer",
            "describe_vtl_devices",
            "describe_working_storage"
        ]
    },
    "support": {
        "List": [],
        "Describe": [
            "describe_attachment",
            "describe_cases",
            "describe_communications",
            "describe_services",
            "describe_severity_levels",
            "describe_trusted_advisor_check_refresh_statuses",
            "describe_trusted_advisor_check_result",
            "describe_trusted_advisor_check_summaries",
            "describe_trusted_advisor_checks"
        ]
    },
    "swf": {
        "List": [
            "list_activity_types",
            "list_closed_workflow_executions",
            "list_domains",
            "list_open_workflow_executions",
            "list_tags_for_resource",
            "list_workflow_types"
        ],
        "Describe": [
            "describe_activity_type",
            "describe_domain",
            "describe_workflow_execution",
            "describe_workflow_type"
        ]
    },
    "synthetics": {
        "List": [
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_canaries",
            "describe_canaries_last_run",
            "describe_runtime_versions"
        ]
    },
    "textract": {
        "List": [],
        "Describe": []
    },
    "timestream-query": {
        "List": [],
        "Describe": [
            "describe_endpoints"
        ]
    },
    "timestream-write": {
        "List": [
            "list_databases",
            "list_tables",
            "list_tags_for_resource"
        ],
        "Describe": [
            "describe_database",
            "describe_endpoints",
            "describe_table"
        ]
    },
    "transcribe": {
        "List": [
            "list_call_analytics_categories",
            "list_call_analytics_jobs",
            "list_language_models",
            "list_medical_transcription_jobs",
            "list_medical_vocabularies",
            "list_tags_for_resource",
            "list_transcription_jobs",
            "list_vocabularies",
            "list_vocabulary_filters"
        ],
        "Describe": [
            "describe_language_model"
        ]
    },
    "transfer": {
        "List": [
            "list_accesses",
            "list_executions",
            "list_security_policies",
            "list_servers",
            "list_tags_for_resource",
            "list_users",
            "list_workflows"
        ],
        "Describe": [
            "describe_access",
            "describe_execution",
            "describe_security_policy",
            "describe_server",
            "describe_user",
            "describe_workflow"
        ]
    },
    "translate": {
        "List": [
            "list_parallel_data",
            "list_terminologies",
            "list_text_translation_jobs"
        ],
        "Describe": [
            "describe_text_translation_job"
        ]
    },
    "waf": {
        "List": [
            "list_activated_rules_in_rule_group",
            "list_byte_match_sets",
            "list_geo_match_sets",
            "list_ip_sets",
            "list_logging_configurations",
            "list_rate_based_rules",
            "list_regex_match_sets",
            "list_regex_pattern_sets",
            "list_rule_groups",
            "list_rules",
            "list_size_constraint_sets",
            "list_sql_injection_match_sets",
            "list_subscribed_rule_groups",
            "list_tags_for_resource",
            "list_web_acls",
            "list_xss_match_sets"
        ],
        "Describe": []
    },
    "waf-regional": {
        "List": [
            "list_activated_rules_in_rule_group",
            "list_byte_match_sets",
            "list_geo_match_sets",
            "list_ip_sets",
            "list_logging_configurations",
            "list_rate_based_rules",
            "list_regex_match_sets",
            "list_regex_pattern_sets",
            "list_resources_for_web_acl",
            "list_rule_groups",
            "list_rules",
            "list_size_constraint_sets",
            "list_sql_injection_match_sets",
            "list_subscribed_rule_groups",
            "list_tags_for_resource",
            "list_web_acls",
            "list_xss_match_sets"
        ],
        "Describe": []
    },
    "wafv2": {
        "List": [
            "list_available_managed_rule_group_versions",
            "list_available_managed_rule_groups",
            "list_ip_sets",
            "list_logging_configurations",
            "list_managed_rule_sets",
            "list_regex_pattern_sets",
            "list_resources_for_web_acl",
            "list_rule_groups",
            "list_tags_for_resource",
            "list_web_acls"
        ],
        "Describe": [
            "describe_managed_rule_group"
        ]
    },
    "wellarchitected": {
        "List": [
            "list_answers",
            "list_lens_review_improvements",
            "list_lens_reviews",
            "list_lenses",
            "list_milestones",
            "list_notifications",
            "list_share_invitations",
            "list_tags_for_resource",
            "list_workload_shares",
            "list_workloads"
        ],
        "Describe": []
    },
    "workdocs": {
        "List": [],
        "Describe": [
            "describe_activities",
            "describe_comments",
            "describe_document_versions",
            "describe_folder_contents",
            "describe_groups",
            "describe_notification_subscriptions",
            "describe_resource_permissions",
            "describe_root_folders",
            "describe_users"
        ]
    },
    "worklink": {
        "List": [
            "list_devices",
            "list_domains",
            "list_fleets",
            "list_tags_for_resource",
            "list_website_authorization_providers",
            "list_website_certificate_authorities"
        ],
        "Describe": [
            "describe_audit_stream_configuration",
            "describe_company_network_configuration",
            "describe_device",
            "describe_device_policy_configuration",
            "describe_domain",
            "describe_fleet_metadata",
            "describe_identity_provider_configuration",
            "describe_website_certificate_authority"
        ]
    },
    "workmail": {
        "List": [
            "list_access_control_rules",
            "list_aliases",
            "list_group_members",
            "list_groups",
            "list_mail_domains",
            "list_mailbox_export_jobs",
            "list_mailbox_permissions",
            "list_mobile_device_access_overrides",
            "list_mobile_device_access_rules",
            "list_organizations",
            "list_resource_delegates",
            "list_resources",
            "list_tags_for_resource",
            "list_users"
        ],
        "Describe": [
            "describe_group",
            "describe_inbound_dmarc_settings",
            "describe_mailbox_export_job",
            "describe_organization",
            "describe_resource",
            "describe_user"
        ]
    },
    "workmailmessageflow": {
        "List": [],
        "Describe": []
    },
    "workspaces": {
        "List": [
            "list_available_management_cidr_ranges"
        ],
        "Describe": [
            "describe_account",
            "describe_account_modifications",
            "describe_client_properties",
            "describe_connection_alias_permissions",
            "describe_connection_aliases",
            "describe_ip_groups",
            "describe_tags",
            "describe_workspace_bundles",
            "describe_workspace_directories",
            "describe_workspace_image_permissions",
            "describe_workspace_images",
            "describe_workspace_snapshots",
            "describe_workspaces",
            "describe_workspaces_connection_status"
        ]
    },
    "xray": {
        "List": [
            "list_tags_for_resource"
        ],
        "Describe": []
    }
}