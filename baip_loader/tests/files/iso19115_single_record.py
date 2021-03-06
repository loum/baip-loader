ISO19115_ITEM = {
    '@xmlns:gco': 'http://www.isotc211.org/2005/gco',
    '@xmlns:gmd': 'http://www.isotc211.org/2005/gmd',
    '@xmlns:gml': 'http://www.opengis.net/gml',
    '@xmlns:gts': 'http://www.isotc211.org/2005/gts',
    '@xmlns:xlink': 'http://www.w3.org/1999/xlink',
    '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    '@xsi:schemaLocation': 'http://www.isotc211.org/2005/gmd http://www.isotc211.org/2005/gmd/gmd.xsd http://www.opengis.net/gml http://www.isotc211.org/2005/gml/gml.xsd http://www.w3.org/1999/xlink http://www.isotc211.org/2005/xlink/xlinks.xsd',
    'gmd:characterSet': {
        'gmd:MD_CharacterSetCode': {
            '#text': 'utf8',
            '@codeList': 'http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#MD_CharacterSetCode',
            '@codeListValue': 'utf8'
        }
    },
    'gmd:contact': {
        'gmd:CI_ResponsibleParty': {
            'gmd:contactInfo': {
                'gmd:CI_Contact': {
                    'gmd:address': {
                        'gmd:CI_Address': {
                            'gmd:administrativeArea': {
                                'gco:CharacterString': 'Vic'
                            },
                            'gmd:city': {
                                'gco:CharacterString': 'East Melbourne'
                            },
                            'gmd:country': {
                                'gco:CharacterString': 'Australia'
                            },
                            'gmd:deliveryPoint': {
                                'gco:CharacterString': 'PO Box 500'
                            },
                            'gmd:electronicMailAddress': {
                                'gco:CharacterString': 'data.vsdl@depi.vic.gov.au'
                            },
                            'gmd:postalCode': {
                                'gco:CharacterString': '3002'
                            }
                        }
                    },
                    'gmd:phone': {
                        'gmd:CI_Telephone': {
                            'gmd:facsimile': {
                                'gco:CharacterString': '86362393'
                            },
                            'gmd:voice': {
                                'gco:CharacterString': '86362385'
                            }
                        }
                    }
                }
            },
            'gmd:individualName': {
                '@gco:nilReason': 'withheld',
                'gco:CharacterString': 'Department of Environment and Primary Industries'
            },
            'gmd:organisationName': {
                'gco:CharacterString': 'VIC - Department of Environment and Primary Industries'
            },
            'gmd:positionName': {
                'gco:CharacterString': 'Dataset Data Manager'
            },
            'gmd:role': {
                'gmd:CI_RoleCode': {
                    '#text': 'pointOfContact',
                    '@codeList': 'http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#CI_RoleCode',
                    '@codeListValue': 'pointOfContact'
                }
            }
        }
    },
    'gmd:dataQualityInfo': {
        'gmd:DQ_DataQuality': {
            'gmd:lineage': {
                'gmd:LI_Lineage': {
                    'gmd:statement': {
                        'gco:CharacterString': u"A number of key input datasets were sourced as part of the process to derive the 3D aquifer surfaces. These datasets included: The DEPI State-wide Stratigraphic Database (SSD); The National Groundwater Information System (NGIS) database containing groundwater borehole location information as well as lithological and stratigraphic information; Raster layers previously produced for Southern Rural Water (SRW) by SKM and GHD in 2009; The crystalline basement surface provided by the former Department of Primary Industries (DPI); Outcrop 1:250,000 scale geological mapping compiled by the former Geological Survey of Victoria, DPI; A state-wide 100m Digital Elevation Model (DEM) based on the DEPI 20m DEM. This was used to represent the natural surface; Data generated using DEPI's state-wide ecoMarkets groundwater modelling package to assist with the definition of key layers of the major Cainozoic aquifers; Latrobe Valley Coal Model which was used to provide a framework for the hydro-stratigraphy of the wet Gippsland Basin; Rasters of the top elevation of the major aquifer systems covering the Kiewa, Ovens, Goulburn-Broken and Loddon and Campaspe catchments; Data extracted from the Basin in a Box, the Murray Basin Hydrological Map Series and the Murray-Darling Basin Groundwater Status 1990-2000: Summary Report; Airborne magnetic data publicly available from raster data published by the former Geological Survey of Victoria, DPI. Once the input data had been compiled, the VAF 3D surfaces were developed by lfollowing a number of key steps, summarised below: (1) Contours as polylines and aquifer extents as polygons were extracted from previous mapping surfaces; (2) Outcrop points attributed with values from the DEM were created; (3) Based on the state-wide stratigraphic database, the contours and extents were refined or created; (4) A top elevation raster was interpolated using contours, outcrop points and bore data then replacing outcrop areas with the DEM; (5) The aquifer thickness was then checked in GIS by comparing layers against each other and assessing for cross-overs and negative thickness; (6) The input data was then revised and bore data, contours, and aquifer extents modified as required due to errors in the thickness; (7) If there were subsequent issues identified such as overlaps between aquifers, mismatches between bores and resulting layers, then the process was revised by returning to Step (3); (8) If the layers were matching well, then extent points were created to smooth layers at the edges; (9) A top elevation raster was generated again using contours, outcrop points, extent points and bore data; (10) The aquifer thickness was checked again, and if significant issues were identified, then the process returned back to Step (3) for further iteration; (11) Further modifications were applied to remove negative thicknesses and to provide minimum thickness of overburden; (12) Top and bottom elevation rasters were then generated at 100m pixel resolution to form the final dataset. In generating each of the layers, a number of Quality Assurance (QA) measures were implemented at various stages of the process. These included a topologic review, a hydrogeological review and an external reveiw by Spatial Vision. The original dataset was published in May 2012 and subsequent revisions have been conducted by Hocking et al and SKM in 2013."
                    }
                }
            },
            'gmd:scope': {
                'gmd:DQ_Scope': {
                    'gmd:level': {
                        'gmd:MD_ScopeCode': {
                            '#text': 'series',
                            '@codeList': 'http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#MD_ScopeCode',
                            '@codeListValue': 'series'
                        }
                    },
                    'gmd:levelDescription': {
                        'gmd:MD_ScopeDescription': {
                            'gmd:other': {
                                'gco:CharacterString': 'series'
                            }
                        }
                    }
                }
            }
        }
    },
    'gmd:dateStamp': {
        'gco:Date': '2015-02-10'
    },
    'gmd:distributionInfo': None,
    'gmd:fileIdentifier': {
        'gco:CharacterString': 'DD006FCE-BEF5-4377-82AE-2C5A14B50E34'
    },
    'gmd:hierarchyLevel': {
        'gmd:MD_ScopeCode': {
            '#text': 'dataset',
            '@codeList': 'http://asdd.ga.gov.au/asdd/profileinfo/GAScopeCodeList.xml#MD_ScopeCode',
            '@codeListValue': 'dataset'
        }
    },
    'gmd:hierarchyLevelName': {
        'gco:CharacterString': None
    },
    'gmd:identificationInfo': {
        'gmd:MD_DataIdentification': {
            'gmd:abstract': {
                'gco:CharacterString': '[This data and its metadata statement were supplied to the Bioregional Assessment Programme by a third part and are presented here as originally supplied.]\n\nThis is the master metadata record for the Victorian Aquifer Framework (VAF) 3D Surfaces dataset. For information on each aquifer surface, please refer to the separate metadata record.\n\nDEPI originally engaged GHD to develop seamless 3D aquifer surfaces for the Victorian Aquifer Framework (VAF). The seamless mapping of aquifers across the state provides the fundamental framework for groundwater resource management, underpins development of a revised management structure for Victoria (the Secure Allocation Future Entitlement project funded by the National Water Commission) and contributes to the data needs of the Bureau of Meteorology National Groundwater Information System (NGIS). \n\nThe original dataset was produced by GHD in 2012 using (in part) data provided by Southern Rural Water Corporation and Goulburn-Murray Water Corporation. It has been subsequently amended by Hocking et al and SKM in 2013.'
            },
            'gmd:characterSet': {
                'gmd:MD_CharacterSetCode': {
                    '#text': 'utf8',
                    '@codeList': 'http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#MD_CharacterSetCode',
                    '@codeListValue': 'utf8'
                }
            },
            'gmd:citation': {
                'gmd:CI_Citation': {
                    'gmd:alternateTitle': {
                        'gco:CharacterString': 'Victorian Aquifer Framework (VAF) 3D Surfaces'
                    },
                    'gmd:date': [
                        {
                            'gmd:CI_Date': {
                                'gmd:date': {
                                    'gco:Date': '2015-02-10'
                                },
                                'gmd:dateType': {
                                    'gmd:CI_DateTypeCode': {
                                        '#text': 'creation',
                                        '@codeList': 'http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#CI_DateTypeCode',
                                        '@codeListValue': 'creation'
                                    }
                                }
                            }
                        },
                        {
                            'gmd:CI_Date': {
                                'gmd:date': {
                                    'gco:Date': '2014-10-24'
                                },
                                'gmd:dateType': {
                                    'gmd:CI_DateTypeCode': {
                                        '#text': 'publication',
                                        '@codeList': 'http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#CI_DateTypeCode',
                                        '@codeListValue': 'publication'
                                    }
                                }
                            }
                        },
                        {
                            'gmd:CI_Date': {
                                'gmd:date': {
                                    'gco:Date': '2015-02-10'
                                },
                                'gmd:dateType': {
                                    'gmd:CI_DateTypeCode': {
                                        '#text': 'revision',
                                        '@codeList': 'http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#CI_DateTypeCode',
                                        '@codeListValue': 'revision'
                                    }
                                }
                            }
                        }
                    ],
                    'gmd:otherCitationDetails': {
                        'gco:CharacterString': None
                    },
                    'gmd:title': {
                        'gco:CharacterString': 'Victorian Aquifer Framework - Salinity'
                    }
                }
            },
            'gmd:descriptiveKeywords': [
                {
                    'gmd:MD_Keywords': {
                        'gmd:keyword': {
                            'gco:CharacterString': 'Victoria'
                        },
                        'gmd:thesaurusName': {
                            'gmd:CI_Citation': {
                                'gmd:citedResponsibleParty': {
                                    'gmd:CI_ResponsibleParty': {
                                        'gmd:organisationName': {
                                            'gco:CharacterString': 'ANZLIC the Spatial Information Council'
                                        },
                                        'gmd:role': {
                                            'gmd:CI_RoleCode': {
                                                '#text': 'custodian',
                                                '@codeList': 'http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#CI_RoleCode',
                                                '@codeListValue': 'custodian'
                                            }
                                        }
                                    }
                                },
                                'gmd:date': {
                                    'gmd:CI_Date': {
                                        'gmd:date': {
                                            'gco:Date': '2015-02-10'
                                        },
                                        'gmd:dateType': {
                                            'gmd:CI_DateTypeCode': {
                                                '#text': 'revision',
                                                '@codeList': 'http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#CI_DateTypeCode',
                                                '@codeListValue': 'revision'
                                            }
                                        }
                                    }
                                },
                                'gmd:edition': {
                                    'gco:CharacterString': 'Version 2.1'
                                },
                                'gmd:editionDate': {
                                    'gco:Date': '2015-02-10'
                                },
                                'gmd:identifier': {
                                    'gmd:MD_Identifier': {
                                        'gmd:code': {
                                            'gco:CharacterString': 'http://asdd.ga.gov.au/asdd/profileinfo/anzlic-jurisdic.xml#anzlic-jurisdic'
                                        }
                                    }
                                },
                                'gmd:title': {
                                    'gco:CharacterString': 'ANZLIC Jurisdictions'
                                }
                            }
                        },
                        'gmd:type': {
                            'gmd:MD_KeywordTypeCode': {
                                '#text': 'theme',
                                '@codeList': 'http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#MD_KeywordTypeCode',
                                '@codeListValue': 'theme'
                            }
                        }
                    }
                },
                None
            ],
            'gmd:extent': {
                'gmd:EX_Extent': {
                    'gmd:geographicElement': {
                        'gmd:EX_GeographicBoundingBox': {
                            'gmd:eastBoundLongitude': {
                                'gco:Decimal': '150'
                            },
                            'gmd:northBoundLatitude': {
                                'gco:Decimal': '-34'
                            },
                            'gmd:southBoundLatitude': {
                                'gco:Decimal': '-39'
                            },
                            'gmd:westBoundLongitude': {
                                'gco:Decimal': '141'
                            }
                        }
                    }
                }
            },
            'gmd:language': {
                'gco:CharacterString': 'eng'
            },
            'gmd:pointOfContact': {
                'gmd:CI_ResponsibleParty': {
                    'gmd:contactInfo': {
                        'gmd:CI_Contact': {
                            'gmd:address': {
                                'gmd:CI_Address': {
                                    'gmd:administrativeArea': {
                                        'gco:CharacterString': 'Vic'
                                    },
                                    'gmd:city': {
                                        'gco:CharacterString': 'East Melbourne'
                                    },
                                    'gmd:country': {
                                        'gco:CharacterString': 'Australia'
                                    },
                                    'gmd:deliveryPoint': {
                                        'gco:CharacterString': 'PO Box 500'
                                    },
                                    'gmd:electronicMailAddress': {
                                        'gco:CharacterString': 'data.vsdl@depi.vic.gov.a'
                                    },
                                    'gmd:postalCode': {
                                        'gco:CharacterString': '3002'
                                    }
                                }
                            },
                            'gmd:phone': {
                                'gmd:CI_Telephone': {
                                    'gmd:facsimile': {
                                        'gco:CharacterString': '86362393'
                                    },
                                    'gmd:voice': {
                                        'gco:CharacterString': '86362385'
                                    }
                                }
                            }
                        }
                    },
                    'gmd:individualName': {
                        '@gco:nilReason': 'withheld',
                        'gco:CharacterString': 'Department of Environment and Primary Industries'
                    },
                    'gmd:organisationName': {
                        'gco:CharacterString': 'VIC - Department of Environment and Primary Industries'
                    },
                    'gmd:positionName': {
                        'gco:CharacterString': 'Dataset Data Manager'
                    },
                    'gmd:role': {
                        'gmd:CI_RoleCode': {
                            '#text': 'pointOfContact',
                            '@codeList': 'http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#CI_RoleCode',
                            '@codeListValue': 'pointOfContact'
                        }
                    }
                }
            },
            'gmd:purpose': {
                'gco:CharacterString': 'Aquifer Name, Aquifer Code, Aquifer Number: Quaternary Aquifer QA 100 Upper Tertiary/Quaternary Basalt Aquifer UTB 101 Upper Tertiary/Quaternary Aquifer UTQA 102 Upper Tertiary/Quaternary Aquitard UTQD 103 Upper Tertiary Aquifer (marine) UTAM 104 Upper Tertiary Aquifer (fluvial) UTAF 105 Upper Tertiary Aquitard UTD 106 Upper Mid-Tertiary Aquifer UMTA 107 Upper Mid-Tertiary Aquitard UMTD 108 Lower Mid-Tertiary Aquifer LMTA 109 (Lower) Tertiary Basalts LTB 112 Lower Mid-Tertiary Aquitard LMTD 110 Lower Tertiary Basalts LTB 112 Lower Tertiary Aquifer LTA 111 Lower Tertiary Basalts LTB 112 Cretaceous and Permian Sediments CPS 113 Mesozoic and Palaeozoic Bedrock BSE 114'
            },
            'gmd:resourceConstraints': [
                None,
                {
                    'gmd:MD_LegalConstraints': {
                        'gmd:accessConstraints': {
                            'gmd:MD_RestrictionCode': {
                                '#text': 'licence',
                                '@codeList': 'http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#MD_RestrictionCode',
                                '@codeListValue': 'licence'
                            }
                        },
                        'gmd:useLimitation': {
                            'gco:CharacterString': '(c) Department of Environment and Primary Industries and licenced for re-use under the Creative Commons Attribution 3.0 Australia licence, http://creativecommons.org/licenses/by/3.0/au/deed.en'
                        }
                    }
                },
                {
                    'gmd:MD_LegalConstraints': {
                        'gmd:useConstraints': {
                            'gmd:MD_RestrictionCode': {
                                '#text': 'licence',
                                '@codeList': 'http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#MD_RestrictionCode',
                                '@codeListValue': 'licence'
                            }
                        },
                        'gmd:useLimitation': {
                            'gco:CharacterString': '(c) Department of Environment and Primary Industries and licenced for re-use under the Creative Commons Attribution 3.0 Australia licence, http://creativecommons.org/licenses/by/3.0/au/deed.en'
                        }
                    }
                }
            ],
            'gmd:resourceMaintenance': {
                'gmd:MD_MaintenanceInformation': {
                    'gmd:dateOfNextUpdate': {
                        'gco:Date': '2015-02-10'
                    },
                    'gmd:maintenanceAndUpdateFrequency': {
                        'gmd:MD_MaintenanceFrequencyCode': {
                            '#text': 'asNeeded',
                            '@codeList': 'http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#MD_MaintenanceFrequencyCode',
                            '@codeListValue': 'asNeeded'
                        }
                    }
                }
            },
            'gmd:spatialRepresentationType': {
                'gmd:MD_SpatialRepresentationTypeCode': {
                    '#text': 'grid',
                    '@codeList': 'http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#MD_SpatialRepresentationTypeCode',
                    '@codeListValue': 'grid'
                }
            },
            'gmd:spatialResolution': {
                'gmd:MD_Resolution': {
                    'gmd:equivalentScale': {
                        'gmd:MD_RepresentativeFraction': {
                            'gmd:denominator': {
                                'gco:Integer': '100'
                            }
                        }
                    }
                }
            },
            'gmd:status': {
                'gmd:MD_ProgressCode': {
                    '#text': 'completed',
                    '@codeList': 'http://asdd.ga.gov.au/asdd/profileinfo/gmxCodelists.xml#MD_ProgressCode',
                    '@codeListValue': 'completed'
                }
            },
            'gmd:topicCategory': {
                'gmd:MD_TopicCategoryCode': 'inlandWaters'
            }
        }
    },
    'gmd:language': {
        'gco:CharacterString': 'eng'
    },
    'gmd:metadataConstraints': None,
    'gmd:metadataStandardName': {
        'gco:CharacterString': 'ANZLIC Metadata Profile: An Australian/New Zealand Profile of AS/NZS ISO 19115:2005, Geographic information - Metadata'
    },
    'gmd:metadataStandardVersion': {
        'gco:CharacterString': '1.1'
    },
    'gmd:referenceSystemInfo': {
        'gmd:MD_ReferenceSystem': {
            'gmd:referenceSystemIdentifier': {
                'gmd:RS_Identifier': {
                    'gmd:code': {
                        'gco:CharacterString': 'Geodetic Datum of Australian 1994'
                    }
                }
            }
        }
    }
}
