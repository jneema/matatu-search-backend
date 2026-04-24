from sqlalchemy.ext.asyncio import AsyncSession


async def create_route(
    db: AsyncSession,
    operator: str,
    origin_key: str,
    destination_key: str,
    description: str,
    stage_keys: list[str],
    freq: int,
    duration: int,
    is_express: bool,
    saccos: dict,
    stages: dict,
):
    from app.models.route import Route, RoutePath

    sacco = saccos.get(operator)
    if sacco is None:
        print(f"Skipping '{description}': sacco '{operator}' not found")
        return None

    origin_stage = stages.get(origin_key)
    dest_stage = stages.get(destination_key)

    if origin_stage is None:
        print(
            f"Skipping '{description}': origin stage '{origin_key}' not found")
        return None
    if dest_stage is None:
        print(
            f"Skipping '{description}': dest stage '{destination_key}' not found")
        return None

    route = Route(
        sacco_id=sacco.id,
        origin_stage_id=origin_stage.id,
        dest_stage_id=dest_stage.id,
        via_description=description,
        departure_frequency_mins=freq,
        avg_duration_mins=duration,
        is_express=is_express,
    )
    db.add(route)
    await db.flush()

    for order, key in enumerate(stage_keys):
        stage = stages.get(key)
        if stage is None:
            print(
                f"  ⚠  Route '{description}': path stage '{key}' not found, skipping stop")
            continue
        db.add(RoutePath(route_id=route.id, stage_id=stage.id, stop_order=order))

    return route


async def seed_routes(db: AsyncSession, saccos: dict, stages: dict) -> None:

    async def r(op, orig, dest, desc, keys, freq, dur, express=False):
        return await create_route(
            db, op, orig, dest, desc, keys, freq, dur, express, saccos, stages
        )

    INNER_IN = [
        "Pangani_inbound", "Mlango Kubwa_inbound", "Muthaiga_inbound",
        "Lumumba Drive_inbound", "Alsops_inbound", "Garden City_inbound",
        "Roasters_inbound", "Roysambu (TRM)_inbound",
    ]
    INNER_OUT = [
        "Roysambu (TRM)_outbound", "Roasters_outbound", "Garden City_outbound",
        "Alsops_outbound", "Lumumba Drive_outbound", "Muthaiga_outbound",
        "Mlango Kubwa_outbound", "Pangani_outbound",
    ]
    OUTER_IN = [
        "Githurai 44_inbound", "Githurai 45_inbound", "Kahawa Barracks_inbound",
        "Kenyatta University_inbound", "Kahawa Sukari_inbound",
        "Ruiru Stage_inbound", "Juja Main Stage_inbound",
    ]
    OUTER_OUT = [
        "Juja Main Stage_outbound", "Ruiru Stage_outbound", "Kahawa Sukari_outbound",
        "Kenyatta University_outbound", "Kahawa Barracks_outbound",
        "Githurai 45_outbound", "Githurai 44_outbound",
    ]

    for op, freq, dur in [
        ("Super Metro", 10, 90),
        ("Zuri",        12, 92),
        ("2NK",         15, 90),
        ("Forward Travellers", 20, 95),
    ]:
        await r(op,
                "Juja Main Stage_inbound", "OTC Terminal_inbound",
                f"Juja → OTC via Thika Rd, all stops [{op}]",
                ["Juja Main Stage_inbound"] + list(reversed(OUTER_IN[:-1])) +
                list(reversed(OUTER_IN[-1:])) +
                ["Ruiru Stage_inbound", "Kahawa Sukari_inbound", "Kenyatta University_inbound",
                    "Kahawa Barracks_inbound", "Githurai 45_inbound", "Githurai 44_inbound",
                    "Roysambu (TRM)_inbound", "Roasters_inbound", "Garden City_inbound",
                    "Alsops_inbound", "Lumumba Drive_inbound", "Muthaiga_inbound",
                    "Mlango Kubwa_inbound", "Pangani_inbound", "OTC Terminal_inbound"],
                freq, dur)

        await r(op,
                "OTC Stage_outbound", "Juja Main Stage_outbound",
                f"OTC → Juja via Thika Rd, all stops [{op}]",
                ["OTC Stage_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
                 "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
                 "Garden City_outbound", "Roasters_outbound", "Roysambu (TRM)_outbound",
                 "Githurai 44_outbound", "Githurai 45_outbound", "Kahawa Barracks_outbound",
                 "Kenyatta University_outbound", "Kahawa Sukari_outbound",
                 "Ruiru Stage_outbound", "Juja Main Stage_outbound"],
                freq, dur)

    await r("Nazigi",
            "Juja Main Stage_inbound", "River Road_inbound",
            "Juja → River Rd via Thika Rd, all stops",
            ["Juja Main Stage_inbound", "Ruiru Stage_inbound", "Kahawa Sukari_inbound",
             "Kenyatta University_inbound", "Kahawa Barracks_inbound", "Githurai 45_inbound",
             "Githurai 44_inbound", "Roysambu (TRM)_inbound", "Roasters_inbound",
             "Garden City_inbound", "Alsops_inbound", "Lumumba Drive_inbound",
             "Muthaiga_inbound", "Mlango Kubwa_inbound", "Pangani_inbound",
             "River Road_inbound"],
            15, 95)

    await r("Nazigi",
            "River Road_outbound", "Juja Main Stage_outbound",
            "River Rd → Juja via Thika Rd, all stops",
            ["River Road_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
             "Garden City_outbound", "Roasters_outbound", "Roysambu (TRM)_outbound",
             "Githurai 44_outbound", "Githurai 45_outbound", "Kahawa Barracks_outbound",
             "Kenyatta University_outbound", "Kahawa Sukari_outbound",
             "Ruiru Stage_outbound", "Juja Main Stage_outbound"],
            15, 95)

    await r("Nicco",
            "Githurai 45_inbound", "River Road_inbound",
            "Githurai 45 → River Rd via Thika Rd",
            ["Githurai 45_inbound", "Githurai 44_inbound", "Roysambu (TRM)_inbound",
             "Roasters_inbound", "Garden City_inbound", "Alsops_inbound",
             "Lumumba Drive_inbound", "Muthaiga_inbound", "Mlango Kubwa_inbound",
             "Pangani_inbound", "River Road_inbound"],
            10, 62)

    await r("Nicco",
            "River Road_outbound", "Githurai 45_outbound",
            "River Rd → Githurai 45 via Thika Rd",
            ["River Road_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
             "Garden City_outbound", "Roasters_outbound", "Roysambu (TRM)_outbound",
             "Githurai 44_outbound", "Githurai 45_outbound"],
            10, 62)

    await r("MTN",
            "Githurai 44_inbound", "OTC Terminal_inbound",
            "Githurai 44 → OTC via Thika Rd",
            ["Githurai 44_inbound", "Roysambu (TRM)_inbound", "Roasters_inbound",
             "Garden City_inbound", "Alsops_inbound", "Lumumba Drive_inbound",
             "Muthaiga_inbound", "Mlango Kubwa_inbound", "Pangani_inbound",
             "OTC Terminal_inbound"],
            10, 58)

    await r("MTN",
            "OTC Stage_outbound", "Githurai 44_outbound",
            "OTC → Githurai 44 via Thika Rd",
            ["OTC Stage_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
             "Garden City_outbound", "Roasters_outbound", "Roysambu (TRM)_outbound",
             "Githurai 44_outbound"],
            10, 58)

    await r("Umoinner",
            "Roysambu (TRM)_inbound", "OTC Terminal_inbound",
            "Roysambu → OTC via Thika Rd",
            ["Roysambu (TRM)_inbound", "Roasters_inbound", "Garden City_inbound",
             "Alsops_inbound", "Lumumba Drive_inbound", "Muthaiga_inbound",
             "Mlango Kubwa_inbound", "Pangani_inbound", "OTC Terminal_inbound"],
            8, 38)

    await r("Umoinner",
            "OTC Stage_outbound", "Roysambu (TRM)_outbound",
            "OTC → Roysambu via Thika Rd",
            ["OTC Stage_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
             "Garden City_outbound", "Roasters_outbound", "Roysambu (TRM)_outbound"],
            8, 38)

    for op, freq in [("Neno", 15), ("Classic", 15)]:
        await r(op,
                "Githurai 44_inbound", "OTC Terminal_inbound",
                f"Githurai 44 → OTC [{op}]",
                ["Githurai 44_inbound", "Roysambu (TRM)_inbound", "Garden City_inbound",
                 "Alsops_inbound", "Lumumba Drive_inbound", "Muthaiga_inbound",
                 "Mlango Kubwa_inbound", "Pangani_inbound", "OTC Terminal_inbound"],
                freq, 55)
        await r(op,
                "OTC Stage_outbound", "Githurai 44_outbound",
                f"OTC → Githurai 44 [{op}]",
                ["OTC Stage_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
                 "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
                 "Garden City_outbound", "Roysambu (TRM)_outbound", "Githurai 44_outbound"],
                freq, 55)

    await r("Thika Express",
            "Thika Stage_inbound", "OTC Terminal_inbound",
            "Thika → OTC Express (Ruiru, Githurai 44, TRM, Pangani)",
            ["Thika Stage_inbound", "Juja Main Stage_inbound", "Ruiru Stage_inbound",
             "Githurai 44_inbound", "Roysambu (TRM)_inbound", "Garden City_inbound",
             "Pangani_inbound", "OTC Terminal_inbound"],
            20, 110, True)

    await r("Thika Express",
            "OTC Stage_outbound", "Thika Stage_outbound",
            "OTC → Thika Express",
            ["OTC Stage_outbound", "Pangani_outbound", "Garden City_outbound",
             "Roysambu (TRM)_outbound", "Githurai 44_outbound", "Ruiru Stage_outbound",
             "Juja Main Stage_outbound", "Thika Stage_outbound"],
            20, 110, True)

    await r("Forward Travellers",
            "Thika Stage_inbound", "OTC Terminal_inbound",
            "Thika → OTC all stops",
            ["Thika Stage_inbound", "Juja Main Stage_inbound", "JKUAT_inbound",
             "Juja Farm_inbound", "Ruiru Stage_inbound", "Kimbo_inbound",
             "Kahawa Sukari_inbound", "Kenyatta University_inbound", "Kahawa Barracks_inbound",
             "Githurai 45_inbound", "Githurai 44_inbound", "Roysambu (TRM)_inbound",
             "Roasters_inbound", "Garden City_inbound", "Alsops_inbound",
             "Lumumba Drive_inbound", "Muthaiga_inbound", "Mlango Kubwa_inbound",
             "Pangani_inbound", "OTC Terminal_inbound"],
            25, 130)

    await r("Forward Travellers",
            "OTC Stage_outbound", "Thika Stage_outbound",
            "OTC → Thika all stops",
            ["OTC Stage_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
             "Garden City_outbound", "Roasters_outbound", "Roysambu (TRM)_outbound",
             "Githurai 44_outbound", "Githurai 45_outbound", "Kahawa Barracks_outbound",
             "Kenyatta University_outbound", "Kahawa Sukari_outbound", "Kimbo_outbound",
             "Ruiru Stage_outbound", "Juja Farm_outbound", "JKUAT_outbound",
             "Juja Main Stage_outbound", "Thika Stage_outbound"],
            25, 130)

    await r("Ruiru Star",
            "Ruiru Stage_inbound", "OTC Terminal_inbound",
            "Ruiru → OTC all stops",
            ["Ruiru Stage_inbound", "Kahawa Sukari_inbound", "Kenyatta University_inbound",
             "Kahawa Barracks_inbound", "Githurai 45_inbound", "Githurai 44_inbound",
             "Roysambu (TRM)_inbound", "Roasters_inbound", "Garden City_inbound",
             "Alsops_inbound", "Lumumba Drive_inbound", "Muthaiga_inbound",
             "Mlango Kubwa_inbound", "Pangani_inbound", "OTC Terminal_inbound"],
            15, 75)

    await r("Ruiru Star",
            "OTC Stage_outbound", "Ruiru Stage_outbound",
            "OTC → Ruiru all stops",
            ["OTC Stage_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
             "Garden City_outbound", "Roasters_outbound", "Roysambu (TRM)_outbound",
             "Githurai 44_outbound", "Githurai 45_outbound", "Kahawa Barracks_outbound",
             "Kenyatta University_outbound", "Kahawa Sukari_outbound", "Ruiru Stage_outbound"],
            15, 75)

    await r("Super Metro",
            "Roysambu (TRM)_inbound", "OTC Terminal_inbound",
            "TRM → OTC Express",
            ["Roysambu (TRM)_inbound", "Garden City_inbound", "Pangani_inbound",
             "OTC Terminal_inbound"],
            8, 32, True)
    await r("Super Metro",
            "OTC Stage_outbound", "Roysambu (TRM)_outbound",
            "OTC → TRM Express",
            ["OTC Stage_outbound", "Pangani_outbound", "Garden City_outbound",
             "Roysambu (TRM)_outbound"],
            8, 32, True)

    await r("Zuri",
            "Githurai 44_inbound", "OTC Terminal_inbound",
            "Githurai 44 → OTC Express",
            ["Githurai 44_inbound", "Roysambu (TRM)_inbound", "Garden City_inbound",
             "Pangani_inbound", "OTC Terminal_inbound"],
            12, 43, True)
    await r("Zuri",
            "OTC Stage_outbound", "Githurai 44_outbound",
            "OTC → Githurai 44 Express",
            ["OTC Stage_outbound", "Pangani_outbound", "Garden City_outbound",
             "Roysambu (TRM)_outbound", "Githurai 44_outbound"],
            12, 43, True)

    await r("Nazigi",
            "Ruiru Stage_inbound", "OTC Terminal_inbound",
            "Ruiru → OTC Express (Githurai 44, TRM, Pangani)",
            ["Ruiru Stage_inbound", "Githurai 44_inbound", "Roysambu (TRM)_inbound",
             "Pangani_inbound", "OTC Terminal_inbound"],
            15, 52, True)
    await r("Nazigi",
            "OTC Stage_outbound", "Ruiru Stage_outbound",
            "OTC → Ruiru Express",
            ["OTC Stage_outbound", "Pangani_outbound", "Roysambu (TRM)_outbound",
             "Githurai 44_outbound", "Ruiru Stage_outbound"],
            15, 52, True)

    await r("Juja Express",
            "Juja Main Stage_inbound", "OTC Terminal_inbound",
            "Juja → OTC Express (Ruiru, G44, TRM, Pangani)",
            ["Juja Main Stage_inbound", "Ruiru Stage_inbound", "Githurai 44_inbound",
             "Roysambu (TRM)_inbound", "Pangani_inbound", "OTC Terminal_inbound"],
            15, 65, True)
    await r("Juja Express",
            "OTC Stage_outbound", "Juja Main Stage_outbound",
            "OTC → Juja Express",
            ["OTC Stage_outbound", "Pangani_outbound", "Roysambu (TRM)_outbound",
             "Githurai 44_outbound", "Ruiru Stage_outbound", "Juja Main Stage_outbound"],
            15, 65, True)

    await r("MTN",
            "Githurai 44_inbound", "River Road_inbound",
            "Githurai 44 → River Rd Express (panya)",
            ["Githurai 44_inbound", "Roysambu (TRM)_inbound", "Pangani_inbound",
             "Globe Cinema_inbound", "River Road_inbound"],
            12, 48, True)
    await r("MTN",
            "River Road_outbound", "Githurai 44_outbound",
            "River Rd → Githurai 44 Express (panya)",
            ["River Road_outbound", "Globe Cinema_outbound", "Pangani_outbound",
             "Roysambu (TRM)_outbound", "Githurai 44_outbound"],
            12, 48, True)

    await r("Nicco",
            "Githurai 45_inbound", "Afya Centre_inbound",
            "Githurai 45 → Afya Centre (panya via Odeon)",
            ["Githurai 45_inbound", "Githurai 44_inbound", "Roysambu (TRM)_inbound",
             "Garden City_inbound", "Alsops_inbound", "Lumumba Drive_inbound",
             "Muthaiga_inbound", "Pangani_inbound", "Odeon_inbound",
             "Ronald Ngala_inbound", "Afya Centre_inbound"],
            12, 68)
    await r("Nicco",
            "Afya Centre_outbound", "Githurai 45_outbound",
            "Afya Centre → Githurai 45 (panya via Odeon)",
            ["Afya Centre_outbound", "Ronald Ngala_outbound", "Odeon_outbound",
             "Pangani_outbound", "Muthaiga_outbound", "Lumumba Drive_outbound",
             "Alsops_outbound", "Garden City_outbound", "Roysambu (TRM)_outbound",
             "Githurai 44_outbound", "Githurai 45_outbound"],
            12, 68)

    await r("Citi Hoppa",
            "Githurai 45_inbound", "OTC Terminal_inbound",
            "Githurai 45 → OTC via Thika Rd",
            ["Githurai 45_inbound", "Githurai 44_inbound", "Roysambu (TRM)_inbound",
             "Roasters_inbound", "Garden City_inbound", "Alsops_inbound",
             "Lumumba Drive_inbound", "Muthaiga_inbound", "Mlango Kubwa_inbound",
             "Pangani_inbound", "OTC Terminal_inbound"],
            10, 60)
    await r("Citi Hoppa",
            "OTC Stage_outbound", "Githurai 45_outbound",
            "OTC → Githurai 45 via Thika Rd",
            ["OTC Stage_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
             "Garden City_outbound", "Roasters_outbound", "Roysambu (TRM)_outbound",
             "Githurai 44_outbound", "Githurai 45_outbound"],
            10, 60)

    await r("Matatu 45",
            "Roysambu (TRM)_inbound", "River Road_inbound",
            "TRM → River Rd, all stops",
            ["Roysambu (TRM)_inbound", "Roasters_inbound", "Garden City_inbound",
             "Alsops_inbound", "Lumumba Drive_inbound", "Muthaiga_inbound",
             "Mlango Kubwa_inbound", "Pangani_inbound", "River Road_inbound"],
            8, 42)
    await r("Matatu 45",
            "River Road_outbound", "Roysambu (TRM)_outbound",
            "River Rd → TRM, all stops",
            ["River Road_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
             "Garden City_outbound", "Roasters_outbound", "Roysambu (TRM)_outbound"],
            8, 42)

    await r("Sasa Sawa",
            "Roysambu (TRM)_inbound", "OTC Terminal_inbound",
            "Sawa Mall → OTC via Thika Rd",
            ["Roysambu (TRM)_inbound", "Roasters_inbound", "Garden City_inbound",
             "Alsops_inbound", "Lumumba Drive_inbound", "Muthaiga_inbound",
             "Mlango Kubwa_inbound", "Pangani_inbound", "OTC Terminal_inbound"],
            10, 40)
    await r("Sasa Sawa",
            "OTC Stage_outbound", "Roysambu (TRM)_outbound",
            "OTC → Sawa Mall via Thika Rd",
            ["OTC Stage_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
             "Garden City_outbound", "Roasters_outbound", "Roysambu (TRM)_outbound"],
            10, 40)

    await r("Sasa Sawa",
            "Roysambu (TRM)_inbound", "River Road_inbound",
            "Sawa Mall → River Rd (panya)",
            ["Roysambu (TRM)_inbound", "Garden City_inbound", "Alsops_inbound",
             "Lumumba Drive_inbound", "Pangani_inbound", "Odeon_inbound",
             "River Road_inbound"],
            12, 45, True)
    await r("Sasa Sawa",
            "River Road_outbound", "Roysambu (TRM)_outbound",
            "River Rd → Sawa Mall (panya)",
            ["River Road_outbound", "Odeon_outbound", "Pangani_outbound",
             "Lumumba Drive_outbound", "Alsops_outbound", "Garden City_outbound",
             "Roysambu (TRM)_outbound"],
            12, 45, True)

    await r("Joy Kenya",
            "Githurai 44_inbound", "River Road_inbound",
            "Githurai 44 → River Rd via Thika Rd",
            ["Githurai 44_inbound", "Roysambu (TRM)_inbound", "Roasters_inbound",
             "Garden City_inbound", "Alsops_inbound", "Lumumba Drive_inbound",
             "Muthaiga_inbound", "Mlango Kubwa_inbound", "Pangani_inbound",
             "River Road_inbound"],
            12, 60)
    await r("Joy Kenya",
            "River Road_outbound", "Githurai 44_outbound",
            "River Rd → Githurai 44 via Thika Rd",
            ["River Road_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
             "Garden City_outbound", "Roasters_outbound", "Roysambu (TRM)_outbound",
             "Githurai 44_outbound"],
            12, 60)

    await r("Kenya Mpya",
            "Githurai 44_inbound", "GPO Drop-off_inbound",
            "Githurai 44 → GPO via Thika Rd",
            ["Githurai 44_inbound", "Roysambu (TRM)_inbound", "Roasters_inbound",
             "Garden City_inbound", "Alsops_inbound", "Lumumba Drive_inbound",
             "Muthaiga_inbound", "Mlango Kubwa_inbound", "Pangani_inbound",
             "GPO Drop-off_inbound"],
            15, 62)
    await r("Kenya Mpya",
            "GPO Pick-up_outbound", "Githurai 44_outbound",
            "GPO → Githurai 44 via Thika Rd",
            ["GPO Pick-up_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
             "Garden City_outbound", "Roasters_outbound", "Roysambu (TRM)_outbound",
             "Githurai 44_outbound"],
            15, 62)

    await r("Metro Trans",
            "Roysambu (TRM)_inbound", "GPO Drop-off_inbound",
            "TRM → GPO (electric bus)",
            ["Roysambu (TRM)_inbound", "Roasters_inbound", "Garden City_inbound",
             "Alsops_inbound", "Lumumba Drive_inbound", "Muthaiga_inbound",
             "Mlango Kubwa_inbound", "Pangani_inbound", "GPO Drop-off_inbound"],
            15, 42)
    await r("Metro Trans",
            "GPO Pick-up_outbound", "Roysambu (TRM)_outbound",
            "GPO → TRM (electric bus)",
            ["GPO Pick-up_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
             "Garden City_outbound", "Roasters_outbound", "Roysambu (TRM)_outbound"],
            15, 42)

    await r("Paradiso",
            "Roysambu (TRM)_inbound", "Afya Centre_inbound",
            "TRM → Afya Centre (14-seater panya)",
            ["Roysambu (TRM)_inbound", "Garden City_inbound", "Lumumba Drive_inbound",
             "Pangani_inbound", "Ronald Ngala_inbound", "Afya Centre_inbound"],
            10, 38, True)
    await r("Paradiso",
            "Afya Centre_outbound", "Roysambu (TRM)_outbound",
            "Afya Centre → TRM (14-seater panya)",
            ["Afya Centre_outbound", "Ronald Ngala_outbound", "Pangani_outbound",
             "Lumumba Drive_outbound", "Garden City_outbound", "Roysambu (TRM)_outbound"],
            10, 38, True)

    ZIM_IN = ["Zimmerman Stage_inbound", "Baraka_inbound", "Snowflake_inbound",
              "Zimmerman Junction_inbound"]
    ZIM_OUT = ["Zimmerman Junction_outbound", "Snowflake_outbound", "Baraka_outbound",
               "Zimmerman Stage_outbound"]

    for op, cbd_in, cbd_out, freq, dur in [
        ("Super Metro",       "OTC Terminal_inbound",  "OTC Stage_outbound",  12, 55),
        ("Zuri",              "OTC Terminal_inbound",  "OTC Stage_outbound",  15, 55),
        ("Nazigi",            "River Road_inbound",
         "River Road_outbound", 15, 58),
        ("Citi Hoppa",        "OTC Terminal_inbound",  "OTC Stage_outbound",  10, 55),
        ("Zimmerman Express", "OTC Terminal_inbound",  "OTC Stage_outbound",  12, 50),
    ]:
        await r(op,
                "Zimmerman Stage_inbound", cbd_in,
                f"Zimmerman → CBD [{op}]",
                ZIM_IN + ["Roysambu (TRM)_inbound", "Roasters_inbound", "Garden City_inbound",
                          "Alsops_inbound", "Lumumba Drive_inbound", "Muthaiga_inbound",
                          "Mlango Kubwa_inbound", "Pangani_inbound", cbd_in],
                freq, dur)
        await r(op,
                cbd_out, "Zimmerman Stage_outbound",
                f"CBD → Zimmerman [{op}]",
                [cbd_out, "Pangani_outbound", "Mlango Kubwa_outbound", "Muthaiga_outbound",
                 "Lumumba Drive_outbound", "Alsops_outbound", "Garden City_outbound",
                 "Roasters_outbound", "Roysambu (TRM)_outbound"] + ZIM_OUT,
                freq, dur)

    await r("Zimmerman Express",
            "Lucky Summer_inbound", "OTC Terminal_inbound",
            "Lucky Summer → OTC (panya inner Zimmerman)",
            ["Lucky Summer_inbound", "Zimmerman Inner_inbound", "Zimmerman Stage_inbound",
             "Zimmerman Junction_inbound", "Roysambu (TRM)_inbound", "Garden City_inbound",
             "Lumumba Drive_inbound", "Pangani_inbound", "OTC Terminal_inbound"],
            15, 58, True)
    await r("Zimmerman Express",
            "OTC Stage_outbound", "Lucky Summer_outbound",
            "OTC → Lucky Summer (panya)",
            ["OTC Stage_outbound", "Pangani_outbound", "Lumumba Drive_outbound",
             "Garden City_inbound", "Roysambu (TRM)_outbound", "Zimmerman Junction_outbound",
             "Zimmerman Stage_outbound", "Zimmerman Inner_outbound", "Lucky Summer_outbound"],
            15, 58, True)

    KW_IN = ["Kahawa West Phase 2_inbound", "Kahawa West Phase 1_inbound",
             "Kahawa West Stage A_inbound", "Gitau Stage_inbound"]
    KW_OUT = ["Gitau Stage_outbound", "Kahawa West Stage A_outbound",
              "Kahawa West Phase 1_outbound", "Kahawa West Phase 2_outbound"]

    for op, extra_in, extra_out, freq, dur in [
        ("Super Metro", ["Kenyatta University_inbound", "Kahawa Barracks_inbound",
                         "Githurai 45_inbound", "Githurai 44_inbound"],
         ["Githurai 44_outbound", "Githurai 45_outbound",
          "Kahawa Barracks_outbound", "Kenyatta University_outbound"],
         12, 75),
        ("Zuri",        ["Kenyatta University_inbound", "Kahawa Barracks_inbound",
                         "Githurai 44_inbound"],
         ["Githurai 44_outbound", "Kahawa Barracks_outbound",
          "Kenyatta University_outbound"],
         15, 75),
        ("2NK",         ["Kenyatta University_inbound", "Kahawa Barracks_inbound",
                         "Githurai 44_inbound"],
         ["Githurai 44_outbound", "Kahawa Barracks_outbound",
          "Kenyatta University_outbound"],
         15, 72),
    ]:
        await r(op,
                "Kahawa West Phase 2_inbound", "OTC Terminal_inbound",
                f"K-West → OTC [{op}]",
                KW_IN + extra_in + ["Roysambu (TRM)_inbound", "Garden City_inbound",
                                    "Alsops_inbound", "Lumumba Drive_inbound", "Muthaiga_inbound",
                                    "Mlango Kubwa_inbound", "Pangani_inbound", "OTC Terminal_inbound"],
                freq, dur)
        await r(op,
                "OTC Stage_outbound", "Kahawa West Phase 2_outbound",
                f"OTC → K-West [{op}]",
                ["OTC Stage_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
                 "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
                 "Garden City_outbound", "Roysambu (TRM)_outbound"] +
                extra_out + KW_OUT,
                freq, dur)

    await r("KU Shuttle",
            "Kahawa West Phase 2_inbound", "Githurai 44_inbound",
            "K-West → Githurai 44 via KU (shuttle)",
            KW_IN + ["Kenyatta University_inbound", "Kahawa Barracks_inbound",
                     "Githurai 45_inbound", "Githurai 44_inbound"],
            15, 30)
    await r("KU Shuttle",
            "Githurai 44_outbound", "Kahawa West Phase 2_outbound",
            "Githurai 44 → K-West via KU (shuttle)",
            ["Githurai 44_outbound", "Githurai 45_outbound", "Kahawa Barracks_outbound",
             "Kenyatta University_outbound"] + KW_OUT,
            15, 30)

    await r("2NK",
            "Kahawa West Bypass_inbound", "OTC Terminal_inbound",
            "K-West Bypass → OTC (panya shortcut)",
            ["Kahawa West Bypass_inbound", "Kahawa West Stage A_inbound",
             "Kenyatta University_inbound", "Githurai 44_inbound",
             "Roysambu (TRM)_inbound", "Pangani_inbound", "OTC Terminal_inbound"],
            20, 65, True)
    await r("2NK",
            "OTC Stage_outbound", "Kahawa West Bypass_outbound",
            "OTC → K-West Bypass (panya)",
            ["OTC Stage_outbound", "Pangani_outbound", "Roysambu (TRM)_outbound",
             "Githurai 44_outbound", "Kenyatta University_outbound",
             "Kahawa West Stage A_outbound", "Kahawa West Bypass_outbound"],
            20, 65, True)

    await r("Super Metro",
            "Mwiki Stage_inbound", "OTC Terminal_inbound",
            "Mwiki → OTC via Kasarani, Thika Rd",
            ["Mwiki Stage_inbound", "Kasarani Stage_inbound", "Garden City_inbound",
             "Alsops_inbound", "Lumumba Drive_inbound", "Muthaiga_inbound",
             "Mlango Kubwa_inbound", "Pangani_inbound", "OTC Terminal_inbound"],
            15, 55)
    await r("Super Metro",
            "OTC Stage_outbound", "Mwiki Stage_outbound",
            "OTC → Mwiki via Thika Rd, Kasarani",
            ["OTC Stage_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
             "Garden City_outbound", "Kasarani Stage_outbound", "Mwiki Stage_outbound"],
            15, 55)

    await r("Citi Hoppa",
            "Hunters_inbound", "OTC Terminal_inbound",
            "Hunters → OTC via Clay City, Mwiki, Kasarani",
            ["Hunters_inbound", "Clay City_inbound", "Mwiki Stage_inbound",
             "Kasarani Stage_inbound", "Garden City_inbound", "Alsops_inbound",
             "Lumumba Drive_inbound", "Muthaiga_inbound", "Mlango Kubwa_inbound",
             "Pangani_inbound", "OTC Terminal_inbound"],
            20, 70)
    await r("Citi Hoppa",
            "OTC Stage_outbound", "Hunters_outbound",
            "OTC → Hunters via Kasarani, Clay City",
            ["OTC Stage_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
             "Garden City_outbound", "Kasarani Stage_outbound", "Mwiki Stage_outbound",
             "Clay City_outbound", "Hunters_outbound"],
            20, 70)

    await r("Kasarani Link",
            "Kasarani Stage_inbound", "OTC Terminal_inbound",
            "Kasarani → OTC via Alsops, Thika Rd",
            ["Kasarani Stage_inbound", "Garden City_inbound", "Alsops_inbound",
             "Lumumba Drive_inbound", "Muthaiga_inbound", "Mlango Kubwa_inbound",
             "Pangani_inbound", "OTC Terminal_inbound"],
            15, 45)
    await r("Kasarani Link",
            "OTC Stage_outbound", "Kasarani Stage_outbound",
            "OTC → Kasarani",
            ["OTC Stage_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
             "Garden City_outbound", "Kasarani Stage_outbound"],
            15, 45)

    await r("Clay City Link",
            "Hunters_inbound", "River Road_inbound",
            "Hunters → River Rd via Clay City, Kasarani (panya)",
            ["Hunters_inbound", "Clay City_inbound", "Sunton_inbound", "Mwiki Stage_inbound",
             "Kasarani Stage_inbound", "Garden City_inbound", "Lumumba Drive_inbound",
             "Pangani_inbound", "Odeon_inbound", "River Road_inbound"],
            20, 72, True)
    await r("Clay City Link",
            "River Road_outbound", "Hunters_outbound",
            "River Rd → Hunters via Kasarani (panya)",
            ["River Road_outbound", "Odeon_outbound", "Pangani_outbound",
             "Lumumba Drive_outbound", "Garden City_outbound", "Kasarani Stage_outbound",
             "Mwiki Stage_outbound", "Sunton_outbound", "Clay City_outbound",
             "Hunters_outbound"],
            20, 72, True)

    await r("Super Metro",
            "Bypass Kamakis_inbound", "OTC Terminal_inbound",
            "Kamakis → OTC via Eastern Bypass",
            ["Bypass Kamakis_inbound", "Bypass Ruiru_inbound", "Garden City_inbound",
             "Alsops_inbound", "Lumumba Drive_inbound", "Muthaiga_inbound",
             "Mlango Kubwa_inbound", "Pangani_inbound", "OTC Terminal_inbound"],
            20, 65)
    await r("Super Metro",
            "OTC Stage_outbound", "Bypass Kamakis_outbound",
            "OTC → Kamakis via Eastern Bypass",
            ["OTC Stage_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
             "Garden City_outbound", "Bypass Ruiru_outbound", "Bypass Kamakis_outbound"],
            20, 65)

    await r("Zuri",
            "Bypass Kamakis_inbound", "River Road_inbound",
            "Kamakis → River Rd via Eastern Bypass",
            ["Bypass Kamakis_inbound", "Bypass Ruiru_inbound", "Kamakis Market_inbound",
             "Garden City_inbound", "Alsops_inbound", "Lumumba Drive_inbound",
             "Muthaiga_inbound", "Mlango Kubwa_inbound", "Pangani_inbound",
             "River Road_inbound"],
            20, 67)
    await r("Zuri",
            "River Road_outbound", "Bypass Kamakis_outbound",
            "River Rd → Kamakis via Eastern Bypass",
            ["River Road_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Lumumba Drive_outbound", "Alsops_outbound",
             "Garden City_outbound", "Kamakis Market_outbound", "Bypass Ruiru_outbound",
             "Bypass Kamakis_outbound"],
            20, 67)

    await r("Matatu Bypass",
            "Utawala Stage_inbound", "OTC Terminal_inbound",
            "Utawala → OTC via Eastern Bypass",
            ["Utawala Stage_inbound", "EPZ_inbound", "Bypass Syokimau_inbound",
             "Bypass Mlolongo_inbound", "OTC Terminal_inbound"],
            20, 52)
    await r("Matatu Bypass",
            "OTC Stage_outbound", "Utawala Stage_outbound",
            "OTC → Utawala via Eastern Bypass",
            ["OTC Stage_outbound", "Bypass Mlolongo_outbound", "Bypass Syokimau_outbound",
             "EPZ_outbound", "Utawala Stage_outbound"],
            20, 52)

    await r("Super Metro",
            "Northern Bypass Ruiru_inbound", "OTC Terminal_inbound",
            "Ruiru → OTC via Northern Bypass, Gigiri, Muthaiga",
            ["Northern Bypass Ruiru_inbound", "Gigiri_inbound", "Windsor_inbound",
             "Runda_inbound", "Garden Estate_inbound", "Muthaiga Mini Market_inbound",
             "Muthaiga_inbound", "Mlango Kubwa_inbound", "Pangani_inbound",
             "OTC Terminal_inbound"],
            20, 70)
    await r("Super Metro",
            "OTC Stage_outbound", "Northern Bypass Ruiru_outbound",
            "OTC → Ruiru via Northern Bypass",
            ["OTC Stage_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Muthaiga Mini Market_outbound", "Garden Estate_outbound",
             "Runda_outbound", "Windsor_outbound", "Gigiri_outbound",
             "Northern Bypass Ruiru_outbound"],
            20, 70)

    await r("Citi Hoppa",
            "Gigiri_inbound", "OTC Terminal_inbound",
            "Gigiri → OTC via Northern Bypass",
            ["Gigiri_inbound", "Windsor_inbound", "Runda_inbound", "Garden Estate_inbound",
             "Muthaiga Mini Market_inbound", "Muthaiga_inbound", "Mlango Kubwa_inbound",
             "Pangani_inbound", "OTC Terminal_inbound"],
            20, 45)
    await r("Citi Hoppa",
            "OTC Stage_outbound", "Gigiri_outbound",
            "OTC → Gigiri via Northern Bypass",
            ["OTC Stage_outbound", "Pangani_outbound", "Mlango Kubwa_outbound",
             "Muthaiga_outbound", "Muthaiga Mini Market_outbound", "Garden Estate_outbound",
             "Runda_outbound", "Windsor_outbound", "Gigiri_outbound"],
            20, 45)

    await db.commit()
