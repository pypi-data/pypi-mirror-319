
from .base_metric_config import BaseMetricConfig, BaseMetricNode
from ..utils import MathOperations


CONTENTOFF_LAYOUT_FILTER = " PageContentLayout in ('Custom - Content off', 'Custom - Headings Only', 'Focus', 'Custom - Content visible on scroll') "
FULL_LAYOUT_FILTER = " PageContentLayout in ('Informational', 'Custom - Content visible') "
PEEK_LAYOUT_FILTER = " PageContentLayout in ('Inspirational Peek', 'Custom - Content Feed Peek', 'Inspirational') "

class MSNMetricTree:
    def __init__(self):
        """
        When adding new metric, need to add the metric to the metric_tree
        Once MSNMetricTree is initialized, the metric_tree will be created.
        TODO: If it's a service code, it should be initialized in the service starting stage, and read all metrics from db.
        TODO: to support multiple metric break down choices.
        """
        self.metric_tree = {
                "UU": [
                MSNMetricTreeNode(metric_name="UU",
                        formula=[],
                        op_type=None,
                        coefficient=[],
                        titan_query="COUNT(DISTINCT (UserMUIDHash, EventDate))",
                        is_direct_query=True)
                ],
                "PV": [
                MSNMetricTreeNode(metric_name="PV",
                        formula=["PV/UU", "UU"],
                        op_type=MathOperations.MULTIPLICATION,
                        coefficient=[1, 1],
                        need_breakdown=[0, 0],
                        titan_query="SUM(IF(UserAction = 'View', 1, 0))",
                        is_direct_query=True)
                ],
                "CPV": [
                MSNMetricTreeNode(metric_name="CPV",
                                formula=["CPV/PV", "PV/UU", "UU"],
                                op_type=MathOperations.MULTIPLICATION,
                                coefficient=[1, 1, 1],
                                need_breakdown=[0, 0, 0],
                                titan_query="SUM(IF(UserAction = 'View', IsCorePV, 0))",
                                is_direct_query=True),
                ],
                "PV/UU": [
                MSNMetricTreeNode(metric_name="PV/UU",
                        formula=["PV", "UU"],
                        op_type=MathOperations.DIVISION,
                        coefficient=[1, 1],
                        titan_query="",
                        is_direct_query=False)
                ],
                "CPV/PV": [
                MSNMetricTreeNode(metric_name="CPV/PV",
                        formula=["CPV", "PV"],
                        op_type=MathOperations.DIVISION,
                        coefficient=[1, 1],
                        titan_query="",
                        is_direct_query=False)
                ],
                "CPV/UU": [
                MSNMetricTreeNode(metric_name="CPV/UU",
                        formula=["CPV/PV", "PV/UU"],
                        op_type=MathOperations.DIVISION,
                        coefficient=[1, 1],
                        need_breakdown=[0, 0],
                        titan_query="",
                        is_direct_query=False)
                ],
                "PV_RequestCount": [
                MSNMetricTreeNode(metric_name="PV_RequestCount",
                        formula=[],
                        op_type=None,
                        coefficient=[],
                        titan_query="COUNT(DISTINCT IF(UserAction = 'View', RequestIdHash, NULL))",
                        is_direct_query=True)
                ],
                "mCFV": [
                MSNMetricTreeNode(metric_name="mCFV", 
                        formula=["mCFV/CPV", "CPV/PV", "PV/UU", "UU"],
                        op_type=MathOperations.MULTIPLICATION, 
                        coefficient=[1, 1, 1, 1], 
                        need_breakdown=[0, 0, 0, 0],
                        titan_query="SUM(mCFV_FY24)", 
                        is_direct_query=True),

                MSNMetricTreeNode(metric_name="mCFV",
                        formula=["landingPagemCFV", "ContentPagemCFV", "VerticalPagemCFV"],
                        op_type=MathOperations.ADDITION,
                        coefficient=[1, 1, 1],
                        need_breakdown = [1, 1, 1],
                        titan_query="SUM(mCFV_FY24)",
                        is_direct_query=True)
                ],

                "mCFV/CPV": [
                MSNMetricTreeNode(metric_name="mCFV/CPV",
                                formula=["mCFV", "CPV"],
                                op_type=MathOperations.DIVISION,
                                coefficient=[1, 1],
                                need_breakdown=[0, 0],
                                titan_query="",
                                is_direct_query=False)
                ], 

                "CSDAU": [
                        MSNMetricTreeNode(metric_name="CSDAU",
                                        formula=["UU", "Visitor/UU", "CSDAU/Visitor"],
                                        op_type=MathOperations.MULTIPLICATION,
                                        coefficient=[1, 1, 1], 
                                        # TODO: TBD
                                        #     titan_query="COUNT(DISTINCT IF(IsMUIDStable = 1 AND EngagementValue = 1 AND multiSearchAnyCaseInsensitive(ContentModuleLineage, ['topsite', 'headersearch','recentsearch', 'managehistory', 'recommendedsites','coachmark', 'notificationcardreceived', 'notificationcardview'] ) = 0 AND NOT (Behavior IN ('Close', 'Hide') AND UserAction in ('NonNavClick', 'Close')), (UserMUIDHash, EventDate), (NULL,NULL)))",
                                        # titan_query= "COUNT(DISTINCT IF(IsCSDAU_FY25 = 1, (UserMUIDHash, EventDate), (NULL,NULL)))",
                                        titan_query="COUNT(DISTINCT IF(IsCSDAU_FY25 = 1 OR (Product like '%windows%' AND Product <> 'windows'AND EventDate >= toDateTime('2024-09-27') AND EventTimeElapsed>7000 AND EventTimeElapsed <= 1000 * 60 * 3 AND IsCorePV = 1 AND EventName <> 'app_error'AND IsMUIDStable = 1), (UserMUIDHash, EventDate), (NULL,NULL)))",
                                        is_direct_query=True)
                        ],
                "Visitor": [
                        MSNMetricTreeNode(metric_name="Visitor",
                                        formula=["Visitor/UU", "UU"],
                                        op_type=MathOperations.MULTIPLICATION,
                                        coefficient=[1, 1],
                                        titan_query="COUNT(DISTINCT IF(IsMUIDStable = 1 OR Canvas in ('Distribution'), (UserMUIDHash, EventDate), (NULL,NULL)))",
                                        is_direct_query=True)
                        ],
                "Visitor/UU": [
                        MSNMetricTreeNode(metric_name="Visitor/UU",
                                        formula=["Visitor", "UU"],
                                        op_type=MathOperations.DIVISION,
                                        coefficient=[1, 1],
                                        titan_query="",
                                        is_direct_query=False)
                ],
                "CSDAU/Visitor": [
                        MSNMetricTreeNode(metric_name="CSDAU/Visitor",
                                        formula=["CSDAU", "Visitor"],
                                        op_type=MathOperations.DIVISION,
                                        coefficient=[1, 1],
                                        titan_query="",
                                        is_direct_query=False)
                        ],
                "LandingPageCSDAU":[
                        MSNMetricTreeNode(metric_name="LandingPageCSDAU",
                                        formula=["DAUByNavClicks", "DAUByScroll", "DAUByNonNavClicks"],  #, "DAUByDwellTime"
                                        op_type=MathOperations.ADDITION,
                                        coefficient=[1,1,1],
                                        titan_query="COUNT(DISTINCT IF(IsMUIDStable = 1 AND EngagementValue = 1 AND UserAction IN ('NonNavClick', 'ImpressionUpdate', 'OnsiteNavClick', 'OffsiteNavClick') AND multiSearchAnyCaseInsensitive(ContentModuleLineage, ['topsite', 'headersearch','recentsearch', 'managehistory', 'recommendedsites','coachmark', 'notificationcardreceived', 'notificationcardview'] ) = 0 AND NOT (Behavior IN ('Close', 'Hide') AND UserAction in ('NonNavClick', 'Close')), (UserMUIDHash, EventDate), (NULL,NULL)))",
                                        is_direct_query=True)
                        ],
                "DAUByNavClicks":[
                        MSNMetricTreeNode(metric_name="DAUByNavClicks",
                                        formula=["OnsiteNavClickUU", "OffsiteNavClickUU"],
                                        op_type=MathOperations.ADDITION,
                                        coefficient=[1, 1],
                                        titan_query="COUNT(DISTINCT IF(IsMUIDStable = 1 AND EngagementValue = 1 AND UserAction IN ('OnsiteNavClick', 'OffsiteNavClick') AND multiSearchAnyCaseInsensitive(ContentModuleLineage, ['topsite', 'headersearch','recentsearch', 'managehistory', 'recommendedsites','coachmark', 'notificationcardreceived', 'notificationcardview'] ) = 0 AND NOT (Behavior IN ('Close', 'Hide') AND UserAction in ('NonNavClick', 'Close')), (UserMUIDHash, EventDate), (NULL,NULL)))",
                                        is_direct_query=True)
                        ],

                "DAUByScroll":[
                        MSNMetricTreeNode(metric_name="DAUByScroll",
                                        formula=[],
                                        op_type=None,
                                        coefficient=[],
                                        titan_query="COUNT(DISTINCT IF(IsMUIDStable = 1 AND EngagementValue = 1 AND Action IN ('Scroll') AND multiSearchAnyCaseInsensitive(ContentModuleLineage, ['topsite', 'headersearch','recentsearch', 'managehistory', 'recommendedsites','coachmark', 'notificationcardreceived', 'notificationcardview'] ) = 0 AND NOT (Behavior IN ('Close', 'Hide') AND UserAction in ('NonNavClick', 'Close')), (UserMUIDHash, EventDate), (NULL,NULL)))",
                                        is_direct_query=True)
                        ],
                "DAUByNonNavClicks":[
                        MSNMetricTreeNode(metric_name="DAUByNonNavClicks",
                                        formula=[],
                                        op_type=None,
                                        coefficient=[],
                                        titan_query="COUNT(DISTINCT IF(IsMUIDStable = 1 AND EngagementValue = 1 AND UserAction IN ('NonNavClick') AND multiSearchAnyCaseInsensitive(ContentModuleLineage, ['topsite', 'headersearch','recentsearch', 'managehistory', 'recommendedsites','coachmark', 'notificationcardreceived', 'notificationcardview'] ) = 0 AND NOT (Behavior IN ('Close', 'Hide') AND UserAction in ('NonNavClick', 'Close')), (UserMUIDHash, EventDate), (NULL,NULL)))",
                                        is_direct_query=True)
                        ],

                "DAUByDwellTime":[
                        MSNMetricTreeNode(metric_name="DAUByDwellTime",
                                                formula=[],
                                                op_type=None,
                                                coefficient=[],
                                                titan_query="""
                                                COUNT(DISTINCT IF(IsMUIDStable = 1 AND EventName <> 'app_error' AND Product <> 'windows' AND 
                                                ((EventTimeElapsed > 10000 AND EventTimeElapsed <= 1000 * 60 * 3 AND IsCorePV = 1 AND (Product like '%windows%' OR (Canvas = 'Lockscreen' AND PageType IN ('ntp','dhp'))))
                                                OR (EventTimeElapsed > 7000 AND EventTimeElapsed <= 1000 * 60 * 3 AND IsCorePV = 1 AND EventDate >= toDateTime('2024-09-27') AND Product like '%windows%'))
                                                , (UserMUIDHash, EventDate), (NULL,NULL)))""",        
                                                is_direct_query=True)
                        ],

                "OnsiteNavClickUU": [
                        MSNMetricTreeNode(metric_name="OnsiteNavClickUU",
                                        formula=["OnsiteNavClicks", "OnsiteNavClicksPerUU"],
                                        op_type=MathOperations.DIVISION,
                                        coefficient=[1, 1],
                                        titan_query = "COUNT(DISTINCT IF(IsMUIDStable = 1 AND EngagementValue = 1 AND UserAction IN ('OnsiteNavClick') AND multiSearchAnyCaseInsensitive(ContentModuleLineage, ['topsite', 'headersearch','recentsearch', 'managehistory', 'recommendedsites','coachmark', 'notificationcardreceived', 'notificationcardview'] ) = 0, (UserMUIDHash, EventDate), (NULL,NULL)))",
                                        # titan_query="COUNT(DISTINCT IF(UserAction = 'OnsiteNavClick', (UserMUIDHash, EventDate), (NULL,NULL)))",
                                        is_direct_query=True)
                        ],
                "OffsiteNavClickUU": [
                        MSNMetricTreeNode(metric_name="OffsiteNavClickUU",
                                        formula=["OffsiteNavClicks", "OffsiteNavClicksPerUU"],
                                        op_type=MathOperations.DIVISION,
                                        coefficient=[1, 1],
                                        titan_query="COUNT(DISTINCT IF(UserAction = 'OffsiteNavClick' AND multiSearchAnyCaseInsensitive(ContentModuleLineage, ['topsite', 'headersearch','recentsearch', 'managehistory', 'recommendedsites','coachmark', 'notificationcardreceived', 'notificationcardview'] ) = 0 , (UserMUIDHash, EventDate), (NULL,NULL)))",
                                        is_direct_query=True)
                        ],
                "OnsiteNavClicks": [
                        MSNMetricTreeNode(metric_name="OnsiteNavClicks",
                                        formula=["ContentNavClicks", "VerticalNavClicks"],
                                                op_type=MathOperations.ADDITION,
                                                coefficient=[1, 1],
                                                titan_query="COUNT(IF(UserAction = 'OnsiteNavClick', UserAction, NULL))",
                                                is_direct_query=True)
                        ],
                "OnsiteNavClicksPerUU": [
                        MSNMetricTreeNode(metric_name="OnsiteNavClicks/UU",
                                        formula=["OnsiteNavClicks", "OnsiteNavClickUU"],
                                        op_type=MathOperations.DIVISION,
                                        coefficient=[1, 1],
                                        titan_query="",
                                        is_direct_query=False)
                        ],
                "OffsiteNavClicks": [
                        MSNMetricTreeNode(metric_name="OffsiteNavClicks",
                                        formula=["OffsiteNavClicksPerUU", "OffsiteNavClickUU"],
                                        op_type=MathOperations.MULTIPLICATION,
                                        coefficient=[1, 1],
                                        titan_query="COUNT(IF(UserAction = 'OffsiteNavClick', UserAction, NULL))",
                                        is_direct_query=True)
                        ],
                "OffsiteNavClicksPerUU": [
                        MSNMetricTreeNode(metric_name="OffsiteNavClicksPerUU",
                                        formula=["OffsiteNavClicks", "OffsiteNavClickUU"],
                                        op_type=MathOperations.DIVISION,
                                        coefficient=[1, 1],
                                        titan_query="",
                                        is_direct_query=False)
                        ],
                "ContentNavClicks": [  # TODO: TBD
                        MSNMetricTreeNode(metric_name="ContentNavClicks",
                                        formula=["ContentNavCTR", "PV_RequestCount"],
                                        op_type=MathOperations.MULTIPLICATION,
                                        coefficient=[1, 1],
                                        titan_query="COUNT(if(UserAction='OnsiteNavClick' and ContentType in ('Article', 'Gallery', 'Watch', 'Video'), UserAction, NULL))",
                                        is_direct_query=True)
                        ],
                "VerticalNavClicks": [  # TODO: TBD
                        MSNMetricTreeNode(metric_name="VerticalNavClicks",
                                        formula=["VerticalNavCTR", "PV_RequestCount"],
                                        op_type=MathOperations.MULTIPLICATION,
                                        coefficient=[1, 1],  
                                        # ContentType = 'StructuredData' AND ContentVertical IS NOT NULL
                                        titan_query="COUNT(if(UserAction='OnsiteNavClick' and ContentType not in ('Article', 'Gallery', 'Watch', 'Video'), UserAction, NULL))",
                                        is_direct_query=True)
                        ],
                "ContentNavCTR": [
                        MSNMetricTreeNode(metric_name="ContentNavCTR",
                                        formula=["ContentNavClicks", "PV_RequestCount"],
                                        op_type=MathOperations.DIVISION,
                                        coefficient=[1, 1],
                                        titan_query="",
                                        is_direct_query=False)
                        ],
                "VerticalNavCTR": [
                        MSNMetricTreeNode(metric_name="VerticalNavCTR",
                                        formula=["VerticalNavClicks", "PV_RequestCount"],
                                        op_type=MathOperations.DIVISION,
                                        coefficient=[1, 1],
                                        titan_query="",
                                        is_direct_query=False)
                        ],

                "FVR": [
                        MSNMetricTreeNode(metric_name="FVR",
                                        formula=["FullLayoutCPVRate", "PeekLayoutCPVRate", "ContentOffCPVRate"],
                                        op_type=MathOperations.ADDITION,
                                        coefficient=[1, 0.33, 0],
                                        # TODO: official FVR in TITAN is different with the following formula
                                        titan_query=f"SUM(multiIf((UserAction = 'View' AND IsCorePV = 1 AND ({FULL_LAYOUT_FILTER} OR Canvas like '%App%')), 1, " \
                                        + f" (UserAction = 'View' AND IsCorePV = 1 AND {PEEK_LAYOUT_FILTER}), 0.33, 0)) "\
                                        + " / SUM(IF(UserAction = 'View', IsCorePV, 0))",
                                        is_direct_query=True),
                                        
                        MSNMetricTreeNode(metric_name="FVR",
                                        formula = [],
                                        op_type=None,
                                        coefficient=[],
                                        titan_query=f"SUM(multiIf((UserAction = 'View' AND IsCorePV = 1 AND ({FULL_LAYOUT_FILTER} OR Canvas like '%App%')), 1, " \
                                        + f" (UserAction = 'View' AND IsCorePV = 1 AND {PEEK_LAYOUT_FILTER}), 0.33, 0)) "\
                                        + " / SUM(IF(UserAction = 'View', IsCorePV, 0))",
                                        is_direct_query=True) 
                        ],
                "FullLayoutCPVRate": [
                                        MSNMetricTreeNode(metric_name="FullLayoutCPVRate",
                                        formula=["FullLayoutCPV", "CPV"],
                                        op_type=MathOperations.DIVISION,
                                        coefficient=[1, 1],
                                        titan_query="",
                                        is_direct_query=False)
                        ],
                "PeekLayoutCPVRate": [
                                MSNMetricTreeNode(metric_name="PeekLayoutCPVRate",
                                formula=["PeekLayoutCPV", "CPV"],
                                op_type=MathOperations.DIVISION,
                                coefficient=[1, 1],
                                titan_query="",
                                is_direct_query=False)
                        ],

                "ContentOffCPVRate": [
                                MSNMetricTreeNode(metric_name="ContentOffCPVRate",
                                formula=["ContentOffCPV", "CPV"],
                                op_type=MathOperations.DIVISION,
                                coefficient=[1, 1],
                                titan_query="",
                                is_direct_query=False)
                        ],

                "FullLayoutPV": [
                                MSNMetricTreeNode(metric_name="FullLayoutPV",
                                formula=["FullLayoutPVPerUU", "FullLayoutUU"],
                                op_type=MathOperations.MULTIPLICATION,
                                coefficient=[1, 1],
                                titan_query = f"SUM(IF(UserAction = 'View' AND ({FULL_LAYOUT_FILTER} OR Canvas like '%App%'), 1, 0))",
                                is_direct_query=True), 
                        ],
                "PeekLayoutPV": [
                                MSNMetricTreeNode(metric_name="PeekLayoutPV",
                                formula=["PeekLayoutPVPerUU", "PeekLayoutUU"],
                                op_type=MathOperations.MULTIPLICATION,
                                coefficient=[1, 1],
                                titan_query = f"SUM(IF(UserAction = 'View' AND {PEEK_LAYOUT_FILTER}, 1, 0))",
                                is_direct_query=True)
                ],
                "ContentOffPV": [
                                MSNMetricTreeNode(metric_name="ContentOffCPV",
                                formula=["ContentOffPVPerUU", "ContentOffUU"],
                                op_type=MathOperations.MULTIPLICATION,
                                coefficient=[1, 1],
                                titan_query = f"SUM(IF(UserAction = 'View' AND {CONTENTOFF_LAYOUT_FILTER}, 1, 0))",
                                is_direct_query=True)
                ],

                "FullLayoutCPV": [
                                MSNMetricTreeNode(metric_name="FullLayoutCPV",
                                formula=["FullLayoutCPVPerPV", "FullLayoutPVPerUU", "FullLayoutUserShare", "UU"],
                                op_type=MathOperations.MULTIPLICATION,
                                coefficient=[1, 1, 1, 1],
                                titan_query= f"SUM(IF(UserAction = 'View' AND IsCorePV = 1 AND ({FULL_LAYOUT_FILTER} OR Canvas like '%App%'), 1, 0))",
                                is_direct_query=True), 
                        ],
                "PeekLayoutCPV": [
                                MSNMetricTreeNode(metric_name="PeekLayoutCPV",
                                formula=["PeekLayoutCPVPerPV", "PeekLayoutPVPerUU", "PeekLayoutUserShare", "UU"],
                                op_type=MathOperations.MULTIPLICATION,
                                coefficient=[1, 1, 1, 1],
                                titan_query = f"SUM(IF(UserAction = 'View' AND IsCorePV = 1 AND {PEEK_LAYOUT_FILTER}, 1, 0))",
                                is_direct_query=True)
                ],
                "ContentOffCPV": [
                                MSNMetricTreeNode(metric_name="ContentOffCPV",
                                formula=["ContentOffCPVPerPV", "ContentOffPVPerUU", "ContentOffUserShare", "UU"],
                                op_type=MathOperations.MULTIPLICATION,
                                coefficient=[1, 1, 1, 1],
                                titan_query = f"SUM(IF(UserAction = 'View' AND IsCorePV = 1 AND {CONTENTOFF_LAYOUT_FILTER}, 1, 0))",
                                is_direct_query=True)
                ],

                "FullLayoutUU": [
                                MSNMetricTreeNode(metric_name="FullLayoutUU",
                                formula=["FullLayoutUserShare", "UU"],
                                op_type=MathOperations.MULTIPLICATION,
                                coefficient=[1, 1],
                                titan_query= f"COUNT(DISTINCT IF({FULL_LAYOUT_FILTER}, (UserMUIDHash, EventDate), (NULL,NULL)))",
                                is_direct_query=True)
                ],
                "PeekLayoutUU": [
                                MSNMetricTreeNode(metric_name="PeekLayoutUU",
                                formula=["PeekLayoutUserShare", "UU"],
                                op_type=MathOperations.MULTIPLICATION,
                                coefficient=[1, 1],
                                titan_query="COUNT(DISTINCT IF(PageContentLayout in ('Inspirational Peek', 'Custom - Content Feed Peek'), (UserMUIDHash, EventDate), (NULL,NULL)))",
                                is_direct_query=True)],

                "ContentOffUU": [
                                MSNMetricTreeNode(metric_name="ContentOffUU",
                                formula=["ContentOffUserShare", "UU"],
                                op_type=MathOperations.MULTIPLICATION,
                                coefficient=[1, 1],
                                titan_query= f"COUNT(DISTINCT IF({CONTENTOFF_LAYOUT_FILTER}, (UserMUIDHash, EventDate), (NULL,NULL)))",
                                is_direct_query=True)
                ],

                "FullLayoutUserShare": [
                                MSNMetricTreeNode(metric_name="FullLayoutUserShare",
                                formula=["FullLayoutUU", "UU"],
                                op_type=MathOperations.DIVISION,
                                coefficient=[1, 1],
                                titan_query="",
                                is_direct_query=False)
                ],

                "PeekLayoutUserShare": [
                                MSNMetricTreeNode(metric_name="PeekLayoutUserShare",
                                formula=["PeekLayoutUU", "UU"],
                                op_type=MathOperations.DIVISION,
                                coefficient=[1, 1],
                                titan_query="",
                                is_direct_query=False)
                ],

                "ContentOffUserShare": [
                                MSNMetricTreeNode(metric_name="ContentOffUserShare",
                                formula=["ContentOffUU", "UU"],
                                op_type=MathOperations.DIVISION,
                                coefficient=[1, 1],
                                titan_query="",
                                is_direct_query=False)
                ],

                "FullLayoutCPVPerPV": [
                                        MSNMetricTreeNode(metric_name="FullLayoutCPVPerPV",
                                        formula=["FullLayoutCPV", "FullLayoutPV"],
                                        op_type=MathOperations.DIVISION,
                                        coefficient=[1, 1],
                                        titan_query="",
                                        is_direct_query=False)
                        ],
                "PeekLayoutCPVPerPV": [
                                        MSNMetricTreeNode(metric_name="PeekLayoutCPVPerPV",
                                        formula=["PeekLayoutCPV", "PeekLayoutPV"],
                                        op_type=MathOperations.DIVISION,
                                        coefficient=[1, 1],
                                        titan_query="",
                                        is_direct_query=False)
                        ],
                "ContentOffCPVPerPV": [
                                        MSNMetricTreeNode(metric_name="ContentOffCPVPerPV",
                                        formula=["ContentOffCPV", "ContentOffPV"],
                                        op_type=MathOperations.DIVISION,
                                        coefficient=[1, 1],
                                        titan_query="",
                                        is_direct_query=False)
                ],
                "FullLayoutPVPerUU": [
                                        MSNMetricTreeNode(metric_name="FullLayoutPVPerUU",
                                        formula=["FullLayoutPV", "FullLayoutUU"],
                                        op_type=MathOperations.DIVISION,
                                        coefficient=[1, 1],
                                        titan_query="",
                                        is_direct_query=False)
                        ],
                "PeekLayoutPVPerUU": [
                                        MSNMetricTreeNode(metric_name="PeekLayoutPVPerUU",
                                        formula=["PeekLayoutPV", "PeekLayoutUU"],
                                        op_type=MathOperations.DIVISION,
                                        coefficient=[1, 1],
                                        titan_query="",
                                        is_direct_query=False)
                        ],
                "ContentOffPVPerUU": [
                        MSNMetricTreeNode(metric_name="ContentOffPVPerUU",
                        formula=["ContentOffPV", "ContentOffUU"],
                        op_type=MathOperations.DIVISION,
                        coefficient=[1, 1],
                        titan_query="",
                        is_direct_query=False)
                ],

        }

    def get_metric_tree(self):
        return self.metric_tree
    

class MSNMetricTreeNode(BaseMetricNode):
    def __init__(self, metric_name, formula, op_type, coefficient, titan_query, is_direct_query=True, need_breakdown=None):
        """
        metric_name: str
        formula: list, the formula of the metric, e.g. ["CPV/UU", "UU"]
        op_type: MathOperations, the operation type of the metric, e.g. MathOperations.MULTIPLICATION
        coefficient: list, the coefficient of the formula, e.g. [1, 1]
        titan_query: str, the query string for titan
        is_direct_query: bool, whether the metric is a direct query or not. If it's not a direct query, the metric will be calculated based on the formula.
        """
        super().__init__()
        if len(formula) != len(coefficient):
            raise ValueError(f"{metric_name}: The length of formula and coefficient should be the same. len(formula): {len(formula)} != len(coefficient): {len(coefficient)}")
        self.metric_name = metric_name
        self.formula = formula
        self.op_type = op_type
        self.coefficient = coefficient
        self.titan_query = titan_query
        self.is_direct_query = is_direct_query

        if not need_breakdown:
            # if need_breakdown is not provided, we assume that we need to break down all the metrics in the formula
            self.need_breakdown = [1 for _ in range(len(formula))]
        else:
            self.need_breakdown = need_breakdown


Titan_Query_Dimension_Template = {
            "Canvas": """CASE WHEN Canvas IN ('Anaheim DHP', 'Anaheim NTP', 'EnterpriseNews NTP') THEN 'All-Up Anaheim'
            WHEN Canvas IN ('WindowsShell Taskbar', 'WindowsP2Shell', 'Enterprise WindowsP2Shell') THEN 'Prong1&2'
            WHEN Canvas IN ('Win 10 Prime', 'Downlevel Prime') THEN 'msn.com'
            WHEN Canvas IN ('AndroidApp', 'IOSApp') THEN 'SuperApp'
            ELSE 'Others' END AS Canvas_""",  # add suffix to avoid conflict with other columns
            
            "Browser": """CASE WHEN lower(Browser) LIKE '%edg%' THEN 'Edge'
            ELSE 'Others' END AS Browser_""",
            
            "PageType": """CASE WHEN lower(PageVertical) == 'homepage' THEN 'Homepage' 
            WHEN lower(PageType) IN ('article', 'gallery', 'video', 'watch') THEN 'Consumption'
            WHEN lower(PageType) NOT IN ('article', 'gallery', 'video', 'watch') 
            AND lower(PageVertical) IN ('sports', 'weather', 'traffic', 'finance', 'casualgames', 'shopping', 'autos') 
            THEN 'Verticals'
            ELSE 'Others' END AS PageType_""",

            "Product": """CASE WHEN Product IN ('anaheim', 'entnews') THEN Product
            WHEN Product IN ('windowsshell', 'windowsdash', 'entwindowsdash', 'windows') THEN Product
            WHEN Product IN ('SuperAppHP', 'SuperAppNews', 'SuperAppBing') THEN Product
            ELSE 'Others' END AS Product_"""
        }

Titan_Query_Dimension_Value_Template = {
    "Canvas": {
        "All-Up Anaheim": "Canvas IN ('Anaheim DHP', 'Anaheim NTP', 'EnterpriseNews NTP')",
        "Prong1&2": "Canvas IN ('WindowsShell Taskbar', 'WindowsP2Shell', 'Enterprise WindowsP2Shell')",
        "msn.com": "Canvas IN ('Win 10 Prime', 'Downlevel Prime')",
        "SuperApp": "Canvas IN ('AndroidApp', 'IOSApp')"
    },
    "Browser": {
        "Edge": "lower(Browser) LIKE '%edg%'"
    },
    "PageType": {
        "Homepage": "lower(PageVertical) == 'homepage'",
        "Consumption": "lower(PageType) IN ('article', 'gallery', 'video', 'watch')",
        "Verticals": """lower(PageType) NOT IN ('article', 'gallery', 'video', 'watch') 
                        AND lower(PageVertical) IN ('sports', 'weather', 'traffic', 'finance', 'casualgames', 'shopping', 'autos')"""
    },
    "Product": {
    }
}