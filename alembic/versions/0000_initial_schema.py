"""create_all_tables
Revision ID: 0000_create_all_tables
Revises:
Create Date: 2026-04-25
"""

from alembic import op  # type: ignore
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0000_create_all_tables"
down_revision = None
branch_labels = None
depends_on = None

routestatus_enum = postgresql.ENUM("active", "suspended", "seasonal",
                                   name="routestatus",   create_type=False)
vehicletype_enum = postgresql.ENUM("14-seater", "32-seater", "52-seater",
                                   "electric",               name="vehicletype",   create_type=False)
operatingstatus_enum = postgresql.ENUM("active", "suspended", "seasonal",
                                       name="operatingstatus", create_type=False)
aliastype_enum = postgresql.ENUM("abbreviation", "colloquial", "former_name",
                                 name="aliastype",     create_type=False)
stagetype_enum = postgresql.ENUM("formal", "informal",
                                 name="stagetype",     create_type=False)
direction_enum = postgresql.ENUM("inbound", "outbound",
                                 name="direction",     create_type=False)
faretype_enum = postgresql.ENUM("peak", "off_peak", "late_night", "weekend",
                                "public_holiday",   name="faretype",      create_type=False)
paymentmethod_enum = postgresql.ENUM("cash", "mpesa", "tap",
                                     name="paymentmethodtype", create_type=False)
alerttype_enum = postgresql.ENUM("short_loop", "delayed", "suspended_temporary",
                                 "diversion",     name="alerttype",     create_type=False)
correctionstatus_enum = postgresql.ENUM("pending", "accepted", "rejected",
                                        name="correctionstatus", create_type=False)

ALL_ENUMS = [
    routestatus_enum,
    vehicletype_enum,
    operatingstatus_enum,
    aliastype_enum,
    stagetype_enum,
    direction_enum,
    faretype_enum,
    paymentmethod_enum,
    alerttype_enum,
    correctionstatus_enum,
]


def upgrade() -> None:
    bind = op.get_bind()

    for enum in ALL_ENUMS:
        enum.create(bind, checkfirst=True)

    op.create_table(
        "saccos",
        sa.Column("id",               postgresql.UUID(
            as_uuid=True), primary_key=True),
        sa.Column("name",             sa.String(
            100),  nullable=False, unique=True),
        sa.Column("vehicle_type",     vehicletype_enum, nullable=False),
        sa.Column("is_electric",      sa.Boolean(),
                  nullable=False, server_default="false"),
        sa.Column("terminus_area",    sa.String(100),  nullable=True),
        sa.Column("operating_status", operatingstatus_enum,
                  nullable=False, server_default="active"),
        sa.Column("safety_rating",    sa.Numeric(2, 1), nullable=True),
        sa.Column("comfort_rating",   sa.Numeric(2, 1), nullable=True),
        sa.Column("is_verified",      sa.Boolean(),
                  nullable=False, server_default="false"),
        sa.Column("last_confirmed_at", sa.DateTime(
            timezone=True), nullable=True),
        sa.Column("created_at",       sa.DateTime(timezone=True),
                  nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "sacco_aliases",
        sa.Column("id",         postgresql.UUID(
            as_uuid=True), primary_key=True),
        sa.Column("sacco_id",   postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("saccos.id"), nullable=False),
        sa.Column("alias",      sa.String(100), nullable=False),
        sa.Column("alias_type", aliastype_enum, nullable=False),
    )

    op.create_table(
        "corridors",
        sa.Column("id",          postgresql.UUID(
            as_uuid=True), primary_key=True),
        sa.Column("name",        sa.String(100), nullable=False, unique=True),
        sa.Column("description", sa.Text(),      nullable=True),
        sa.Column("is_active",   sa.Boolean(),
                  nullable=False, server_default="true"),
    )

    op.create_table(
        "stages",
        sa.Column("id",           postgresql.UUID(
            as_uuid=True), primary_key=True),
        sa.Column("name",         sa.String(150), nullable=False),
        sa.Column("area",         sa.String(100), nullable=False),
        sa.Column("landmark",     sa.String(300), nullable=True),
        sa.Column("landmark_sw",  sa.String(300), nullable=True),
        sa.Column("stage_type",   stagetype_enum, nullable=False),
        sa.Column("direction",    direction_enum,
                  nullable=False),   # dropped in 0001
        sa.Column("latitude",     sa.Numeric(9, 6), nullable=False),
        sa.Column("longitude",    sa.Numeric(9, 6), nullable=False),
        sa.Column("is_active",    sa.Boolean(),
                  nullable=False, server_default="true"),
    )

    op.create_table(
        "stage_hours",
        sa.Column("id",          postgresql.UUID(
            as_uuid=True), primary_key=True),
        sa.Column("stage_id",    postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("stages.id"), nullable=False),
        sa.Column("day_of_week", sa.SmallInteger(), nullable=False),
        sa.Column("open_from",   sa.Time(),          nullable=False),
        sa.Column("open_until",  sa.Time(),          nullable=False),
    )

    op.create_table(
        "routes",
        sa.Column("id",                       postgresql.UUID(
            as_uuid=True), primary_key=True),
        sa.Column("sacco_id",                 postgresql.UUID(
            as_uuid=True), sa.ForeignKey("saccos.id"),    nullable=False),
        sa.Column("corridor_id",              postgresql.UUID(
            as_uuid=True), sa.ForeignKey("corridors.id"), nullable=True),
        sa.Column("origin_stage_id",          postgresql.UUID(
            as_uuid=True), sa.ForeignKey("stages.id"),   nullable=False),
        sa.Column("dest_stage_id",            postgresql.UUID(
            as_uuid=True), sa.ForeignKey("stages.id"),   nullable=False),
        sa.Column("via_description",          sa.String(200),  nullable=True),
        sa.Column("via_description_sw",       sa.String(200),  nullable=True),
        sa.Column("distance_km",              sa.Numeric(6, 2), nullable=True),
        sa.Column("is_express",               sa.Boolean(),
                  nullable=False, server_default="false"),
        sa.Column("route_status",             routestatus_enum,
                  nullable=False, server_default="active"),
        sa.Column("departure_frequency_mins",
                  sa.SmallInteger(), nullable=True),
        sa.Column("avg_duration_mins",
                  sa.SmallInteger(), nullable=True),
        sa.Column("peak_duration_mins",
                  sa.SmallInteger(), nullable=True),
        sa.Column("fare_last_verified_at",    sa.DateTime(
            timezone=True), nullable=True),
        sa.Column("last_confirmed_at",        sa.DateTime(
            timezone=True), nullable=True),
        sa.Column("created_at",               sa.DateTime(
            timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "route_paths",
        sa.Column("id",         postgresql.UUID(
            as_uuid=True), primary_key=True),
        sa.Column("route_id",   postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("routes.id"),  nullable=False),
        sa.Column("stage_id",   postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("stages.id"),  nullable=False),
        sa.Column("stop_order", sa.SmallInteger(), nullable=False),
    )

    op.create_table(
        "transfers",
        sa.Column("id",                  postgresql.UUID(
            as_uuid=True), primary_key=True),
        sa.Column("leg1_route_id",       postgresql.UUID(
            as_uuid=True), sa.ForeignKey("routes.id"), nullable=False),
        sa.Column("leg2_route_id",       postgresql.UUID(
            as_uuid=True), sa.ForeignKey("routes.id"), nullable=False),
        sa.Column("transfer_stage_id",   postgresql.UUID(
            as_uuid=True), sa.ForeignKey("stages.id"), nullable=False),
        sa.Column("avg_wait_mins",       sa.SmallInteger(), nullable=True),
        sa.Column("total_fare_kes",      sa.SmallInteger(), nullable=True),
        sa.Column("is_active",           sa.Boolean(),
                  nullable=False, server_default="true"),
    )

    op.create_table(
        "fares",
        sa.Column("id",          postgresql.UUID(
            as_uuid=True), primary_key=True),
        sa.Column("route_id",    postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("routes.id"), nullable=False),
        sa.Column("fare_type",   faretype_enum,   nullable=False),
        sa.Column("day_type",    sa.SmallInteger(), nullable=False),
        sa.Column("amount_kes",  sa.SmallInteger(), nullable=False),
        sa.Column("valid_from",  sa.Time(),          nullable=False),
        sa.Column("valid_until", sa.Time(),          nullable=False),
    )

    op.create_table(
        "payment_methods",
        sa.Column("id",       postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("route_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("routes.id"), nullable=False),
        sa.Column("method",   paymentmethod_enum, nullable=False),
    )

    op.create_table(
        "public_holidays",
        sa.Column("id",           postgresql.UUID(
            as_uuid=True), primary_key=True),
        sa.Column("name",         sa.String(100), nullable=False),
        sa.Column("holiday_date", sa.Date(),      nullable=False, unique=True),
        sa.Column("is_recurring", sa.Boolean(),
                  nullable=False, server_default="true"),
        sa.Column("year",         sa.SmallInteger(), nullable=True),
    )

    op.create_table(
        "route_alerts",
        sa.Column("id",           postgresql.UUID(
            as_uuid=True), primary_key=True),
        sa.Column("route_id",     postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("routes.id"), nullable=False),
        sa.Column("alert_type",   alerttype_enum, nullable=False),
        sa.Column("message",      sa.Text(),      nullable=False),
        sa.Column("message_sw",   sa.Text(),      nullable=True),
        sa.Column("triggered_by", sa.String(100), nullable=False),
        sa.Column("active_from",  sa.DateTime(timezone=True), nullable=False),
        sa.Column("active_until", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active",    sa.Boolean(),
                  nullable=False, server_default="true"),
        sa.Column("created_at",   sa.DateTime(timezone=True),
                  nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "corridor_surges",
        sa.Column("id",           postgresql.UUID(
            as_uuid=True), primary_key=True),
        sa.Column("corridor_id",  postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("corridors.id"), nullable=False),
        sa.Column("multiplier",   sa.Numeric(4, 2), nullable=False),
        sa.Column("reason",       sa.String(200),   nullable=False),
        sa.Column("reason_sw",    sa.String(200),   nullable=True),
        sa.Column("triggered_by", sa.String(100),   nullable=False),
        sa.Column("active_from",  sa.DateTime(timezone=True), nullable=False),
        sa.Column("active_until", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active",    sa.Boolean(),
                  nullable=False, server_default="true"),
        sa.Column("created_at",   sa.DateTime(timezone=True),
                  nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "occupancy",
        sa.Column("id",              postgresql.UUID(
            as_uuid=True), primary_key=True),
        sa.Column("route_id",        postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("routes.id"), nullable=False),
        sa.Column("day_of_week",     sa.SmallInteger(), nullable=False),
        sa.Column("hour_slot",       sa.SmallInteger(), nullable=False),
        sa.Column("avg_load_factor", sa.Numeric(3, 2),  nullable=False),
        sa.Column("sample_count",    sa.Integer(),
                  nullable=False, server_default="0"),
        sa.Column("updated_at",      sa.DateTime(
            timezone=True), nullable=True),
    )

    op.create_table(
        "fare_corrections",
        sa.Column("id",                   postgresql.UUID(
            as_uuid=True), primary_key=True),
        sa.Column("route_id",             postgresql.UUID(
            as_uuid=True), sa.ForeignKey("routes.id"), nullable=False),
        sa.Column("reported_amount_kes",  sa.SmallInteger(), nullable=False),
        sa.Column("fare_type",            sa.String(50),
                  nullable=False),   # migrated to enum in 0001
        sa.Column("reported_at",          sa.DateTime(
            timezone=True), nullable=False),
        sa.Column("status",               correctionstatus_enum,
                  nullable=False, server_default="pending"),
        sa.Column("device_fingerprint",   sa.String(64),     nullable=True),
    )

    op.create_table(
        "search_logs",
        sa.Column("id",                  postgresql.UUID(
            as_uuid=True), primary_key=True),
        sa.Column("origin_text",         sa.String(200), nullable=False),
        sa.Column("destination_text",    sa.String(200), nullable=False),
        sa.Column("resolved_origin_id",  postgresql.UUID(
            as_uuid=True), nullable=True),
        sa.Column("resolved_dest_id",    postgresql.UUID(
            as_uuid=True), nullable=True),
        sa.Column("result_count",        sa.SmallInteger(), nullable=False),
        sa.Column("had_transfer",        sa.Boolean(),      nullable=True),
        sa.Column("session_id",          sa.String(64),     nullable=True),
        sa.Column("queried_at",          sa.DateTime(
            timezone=True), nullable=False),
    )

    op.create_table(
        "app_settings",
        sa.Column("key",         sa.String(100), primary_key=True),
        sa.Column("value",       sa.Text(),      nullable=False),
        sa.Column("description", sa.Text(),      nullable=True),
        sa.Column("updated_at",  sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_by",  sa.String(100), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("app_settings")
    op.drop_table("search_logs")
    op.drop_table("fare_corrections")
    op.drop_table("occupancy")
    op.drop_table("corridor_surges")
    op.drop_table("route_alerts")
    op.drop_table("public_holidays")
    op.drop_table("payment_methods")
    op.drop_table("fares")
    op.drop_table("transfers")
    op.drop_table("route_paths")
    op.drop_table("routes")
    op.drop_table("stage_hours")
    op.drop_table("stages")
    op.drop_table("corridors")
    op.drop_table("sacco_aliases")
    op.drop_table("saccos")

    bind = op.get_bind()
    for enum in reversed(ALL_ENUMS):
        enum.drop(bind, checkfirst=True)
