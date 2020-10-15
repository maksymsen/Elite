import requests, json, pprint

# with open('systemsPopulated.json') as systemsPopulated_file:
#     local_systems_populated = json.load(systemsPopulated_file)

systems_populated_api = "https://eddb.io/archive/v6/systems_populated.json"
systems_populated = requests.get(systems_populated_api).json()

local_system_data = []
threat_data = []
threat_retreat = []
threat_influence = []
threat_expansion = []
expansion_cube_size = 40

while True:
    option = input('[expansion (e) , threats (t)], retreats (r): ')
    if option == 'expansion' or option == 'e':
        expansion_origin = input('Please enter the name of the system: ')
        if(expansion_origin):
            system_parameters = {'systemName': expansion_origin, 'size':expansion_cube_size}
            systems_cube = requests.get("https://www.edsm.net/api-v1/cube-systems", params=system_parameters).json()
            reference_system = {}
            reference_system_faction_id = None
            for s in systems_populated:
                for cube in systems_cube:
                    if cube['distance'] == 0:
                        reference_system = cube
                if s['name'] == reference_system['name']:
                    # reference_system_faction_id = s['controllingFaction']['id']
                    reference_system_faction_id = s['controlling_minor_faction_id']
            for systems in systems_populated:
                for expansion_systems in systems_cube:
                    if systems['name'] == expansion_systems['name']:
                        # if systems['controllingFaction']['id'] != reference_system_faction_id:
                        if systems['controlling_minor_faction_id'] != reference_system_faction_id:
                            faction_count = 0
                            reference_faction_present = False
                            # for faction_data in systems['factions']:
                            for faction_data in systems['minor_faction_presences']:
                                if faction_data['influence'] > 0:
                                    # if faction_data['id'] != reference_system_faction_id:
                                    if faction_data['minor_faction_id'] != reference_system_faction_id:
                                        faction_count += 1
                                    else:
                                        reference_faction_present = True
                            if faction_count < 7 and reference_faction_present == False:
                                local_system_data.append(systems['name'])
                        continue
            # pprint.pprint(local_system_data)
            for data in local_system_data:
                for cube in systems_cube:
                    if cube['name'] == data:
                        threat_expansion.append(cube)
        for sort in sorted(threat_expansion, key = lambda i: i['distance']):
            print('System: %s, Distance: %s' %(sort['name'], sort['distance']))
        local_system_data = []
        threat_expansion = []
        print('***********************************************************************')
        # *********************************************************************************************************************************************************
    if option == 'threats' or option == 't':
        expansion_origin = input('Please enter the name of the system: ')
        if(expansion_origin):
            system_parameters = {'systemName': expansion_origin, 'size': expansion_cube_size}
            systems_cube = requests.get("https://www.edsm.net/api-v1/cube-systems", params=system_parameters).json()
            for systems in systems_populated:  
                for expansion_systems in systems_cube:
                    if systems['name'] == expansion_systems['name']:
                        faction_count = 0
                        expansion_candidate = False
                        potential_threat = False
                        # for faction_data in systems['factions']:
                        for faction_data in systems['minor_faction_presences']:
                            if faction_data['influence'] > 0:
                                # faction_data['minor_faction_id'] != [x for x in minor_faction_ids if x == faction_data['minor_faction_id']]:
                                faction_count += 1
                                # if faction_data['influence'] > 0.60 and faction_data['state'] == 'Expansion':
                                if faction_data['influence'] > 60:
                                    for states in faction_data['active_states'] or states in faction_data['pending_states']:
                                        if states['name'] == "Expansion":
                                            expansion_candidate = True
                                    # expansion_candidate = True
                                    if expansion_candidate == False:
                                        potential_threat = True
                                    break
                        if faction_count < 8 and expansion_candidate:
                            local_system_data.append(systems['name'])
                        if faction_count < 8 and potential_threat:
                            threat_data.append(systems['name'])
            # pprint.pprint(local_system_data)
            for data in local_system_data:
                for cube in systems_cube:
                    if cube['name'] == data:
                        threat_expansion.append(cube)
            for threat in threat_data:
                for cube in systems_cube:
                    if cube['name'] == threat:
                        threat_influence.append(cube)
        print('***********************************************************************')
        print('Expanding systems: ')
        for sort in sorted(threat_expansion, key = lambda i: i['distance']):
            print('System: %s, Distance: %s' %(sort['name'], sort['distance']))
        print('\nThreats: ')
        for nSort in sorted(threat_influence, key = lambda i: i['distance']):
            print('System: %s, Distance: %s' %(nSort['name'], nSort['distance']))
        local_system_data = []
        threat_expansion = []
        threat_influence = []
        threat_data = []
        print('***********************************************************************')
    # *********************************************************************************************************************************************************
    if option == 'retreats' or option == 'r':
        expansion_origin = input('Please enter the name of the system: ')
        if(expansion_origin):
            system_parameters = {'systemName': expansion_origin, 'size': expansion_cube_size}
            systems_cube = requests.get("https://www.edsm.net/api-v1/cube-systems", params=system_parameters).json()
            for systems in systems_populated:  
                for expansion_systems in systems_cube:
                    if systems['name'] == expansion_systems['name']:
                        faction_count = 0
                        retreat_candidate = False
                        potential_threat = False
                        # for faction_data in systems['factions']:
                        for faction_data in systems['minor_faction_presences']:
                            if faction_data['influence'] > 0:
                                # faction_data['minor_faction_id'] != [x for x in minor_faction_ids if x == faction_data['minor_faction_id']]:
                                faction_count += 1
                                # if faction_data['influence'] > 0.60 and faction_data['state'] == 'Expansion':
                                if faction_data['influence'] < 8:
                                    for states in faction_data['active_states'] or states in faction_data['pending_states']:
                                        if states['name'] == "Retreat":
                                            retreat_candidate = True
                                    # expansion_candidate = True
                                    if retreat_candidate == False:
                                        potential_threat = True
                                    break
                        if faction_count < 8 and retreat_candidate:
                            threat_retreat.append({'system':systems['name'], 'faction_id':faction_data['minor_faction_id'], 'influence': faction_data['influence']})
                        if faction_count < 8 and potential_threat:
                            threat_data.append({'system':systems['name'], 'faction_id':faction_data['minor_faction_id'], 'influence': faction_data['influence']})
            # pprint.pprint(local_system_data)
            # for data in local_system_data:
            #     for cube in systems_cube:
            #         if cube['name'] == data:
            #             threat_expansion.append(cube)
            # for threat in threat_data:
            #     for cube in systems_cube:
            #         if cube['name'] == threat:
            #             threat_influence.append(cube)
        print('***********************************************************************')
        print('Retreating systems: ')
        for sort in sorted(threat_retreat, key= lambda i: i['influence']):
            print(sort)

        print('\nSystems at risk: ')
        for sort in sorted(threat_data, key= lambda i: i['influence']):
            print(sort)
        # for sort in sorted(threat_expansion, key = lambda i: i['distance']):
        #     print('System: %s, Distance: %s' %(sort['name'], sort['distance']))
        # print('\nSystems < 8%: ')
        # for nSort in sorted(threat_influence, key = lambda i: i['distance']):
        #     print('System: %s, Distance: %s' %(nSort['name'], nSort['distance']))
        local_system_data = []
        threat_expansion = []
        threat_retreat = []
        threat_influence = []
        threat_data = []
        print('***********************************************************************')
    # *********************************************************************************************************************************************************
    # if option == 'invasion' or option == 'i':
    #     expansion_origin = input('Please enter the name of the system: ')
    #     if(expansion_origin):
    #         system_parameters = {'systemName': expansion_origin, 'size': expansion_cube_size}
    #         systems_cube = requests.get("https://www.edsm.net/api-v1/cube-systems", params=system_parameters).json()

    #         for systems in systems_populated:  
    #             for expansion_systems in systems_cube:
    #                 if systems['name'] == expansion_systems['name']:
    #                     faction_count = 0
    #                     # for faction_data in systems['factions']:
    #                     for faction_data in systems['minor_faction_presences']:
    #                         if faction_data['influence'] > 0:
    #                             faction_count += 1
    #                     if faction_count < 8:
    #                         local_system_data.append(systems['name'])
    #         # pprint.pprint(local_system_data)
    #         for data in local_system_data:
    #             for cube in systems_cube:
    #                 if cube['name'] == data:
    #                     threat_expansion.append(cube)
    #     for sort in sorted(threat_expansion, key = lambda i: i['distance']):
    #         print(sort)
    #     local_system_data = []
    #     threat_expansion = []
    #     print('***********************************************************************')

    # Invasion temporarily on hold pending a way to figure out how to quickly check if a given faction is native to the system.