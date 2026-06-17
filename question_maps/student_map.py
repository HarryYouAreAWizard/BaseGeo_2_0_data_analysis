

"""find which index in the 2026 data, that correspond to the same question as the index in the 2019 data"""


map = {
    7: 5,   # 7    2019: Be engaging                                                                                              | 7    2026: Consist of courses that integrate well
    8: 6,   # 8    2019: Be academically challenging                                                                              | 8    2026: Have skilled teachers
    9: 7,   # 9    2019: Consist of courses that integrate well                                                                   | 9    2026: How well do you know iEarth?.I have been involved as a student partner
    10:8,   # 10    2019: Have skilled teachers              
# 11:    # 2019: Spatial skills (romlig forståelse)                                                                       | 11    2026: How well do you know iEarth?.I have an idea about what is
12:30,    # 2019: Fieldwork skills                                                                                         | 12    2026: How well do you know iEarth?.I have heard someone mention it, but I am not sure 
13:31,    # 2019: Laboratory skills                                                                                        | 13    2026: How well do you know iEarth?.I have no idea / never heard of it 
14:32,    # 2019: Modelling/computing skills                                                                               | 14    2026: National courses (GeoPraksis/RealfagsPraksis, Geofare Kurs)
# 15    # 2019: Critical thinking                                                                                        | 15    2026: GeoLearning conferences
16:35,    # 2019: Theoretical understanding                                                                                | 16    2026: GeOrakel student activity
# 17:36 ill defined   # 2019: Collaborative skills                                                                                     | 17    2026: Career day
# 18    # 2019: Working in interdisciplinary teams                                                                       | 18    2026: Student assistant in courses
# 19    # 2019: Scientific writing and reading competence (literacy)                                                     | 19    2026: Have you initiated or participated in other local/national initiatives regarding teaching and learning?
# 20:34 ill defined    # 2019: Working with large data sets (ability to interpret data)                                                 | 20    2026: In your opinion, what was the most significant impact of iEarth?
# 21    # 2019: Presentation skills (oral)                                                                               | 21    2026: The geoscience department at UiT
22:37,    # 2019: Communicating scientific/technical content       
    # when students evaluate how much they learn 
    27    2019: Spatial skills (romlig forståelse).1                                                                     | 27    2026: Other geoscience departments at Norwegian universities
    28    2019: Fieldwork skills.1                                                                                       | 28    2026: Other geoscience departments at non-Norwegian universities (international) 
    29    2019: Laboratory skills.1                                                                                      | 29    2026: Research institutions
    30    2019: Modelling/computing skills.1                                                                             | 30    2026:  Fieldwork skills
    31    2019: Critical thinking.1                                                                                      | 31    2026: Laboratory skills
    32    2019: Theoretical understanding.1                                                                              | 32    2026: Modelling/computing skills
    33    2019: Collaborative skills.1                                                                                   | 33    2026: AI-competence 
    34    2019: Working in teams                                                                                         | 34    2026: Quantitative competence (ability to interpret data /numeracy)
    35    2019: Scientific writing and reading competence (literacy).1                                                   | 35    2026: Theoretical understanding
    36    2019: Working with large data sets (ability to interpret data).1                                               | 36    2026: Collaborating in teams
    37    2019: Presentations skills (oral)                                                                              | 37    2026: Communicating scientific/technical content
    38    2019: Communicating scientific/technical content.1         




}
