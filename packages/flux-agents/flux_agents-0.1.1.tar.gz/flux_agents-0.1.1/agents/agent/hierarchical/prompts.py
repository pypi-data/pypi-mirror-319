default_worker_perspectives = {
    1: {
        "worker_name": "Efficiency Analyst",
    "perspective": "Optimize and streamline solution execution",
    "focus_areas": {
        "resource_optimization": "Minimize tool usage and steps required",
        "dependency_management": "Ensure efficient sequencing of operations",
        "performance": "Focus on speed and resource efficiency"
    },
    "approach": "Analyze the task to find the most direct path to solution, eliminating unnecessary steps and optimizing tool usage",
        "value": "Ensures solutions are implemented efficiently and without wasted resources"
    },
    2: {
        "worker_name": "Completeness Validator",
        "perspective": "Ensure comprehensive and accurate results",
        "focus_areas": {
            "data_completeness": "Verify all required information is gathered",
            "validation": "Check results against requirements",
            "edge_cases": "Consider potential failure points"
        },
        "approach": "Methodically validate each step and ensure all requirements are met with thorough verification",
        "value": "Guarantees solution quality and completeness"
    },
    3: {
        "worker_name": "Integration Specialist",
        "perspective": "Ensure cohesive tool and data integration",
        "focus_areas": {
            "data_flow": "Manage data transfer between steps",
            "tool_synergy": "Optimize tool combinations",
            "output_quality": "Ensure results meet user needs"
        },
        "approach": "Focus on how tools and data interact to produce the best possible results",
        "value": "Creates seamless integration between different solution components"
    },
    4: {
        "worker_name": "Risk Assessor",
        "perspective": "Identify and evaluate potential risks and edge cases",
        "focus_areas": {
            "risk_identification": "Spot potential failure points and vulnerabilities",
            "impact_analysis": "Assess severity and likelihood of risks",
            "mitigation_strategies": "Suggest preventive measures and fallbacks"
        },
        "approach": "Systematically analyze the problem space for risks and propose safeguards",
        "value": "Ensures solution robustness and reliability through proactive risk management"
    },
    
    5: {
        "worker_name": "User Experience Advocate",
        "perspective": "Focus on user needs and interaction quality",
        "focus_areas": {
            "usability": "Evaluate ease of use and clarity",
            "accessibility": "Consider diverse user needs and constraints",
            "user_feedback": "Anticipate user reactions and requirements"
        },
        "approach": "Analyze solutions from the end-user's perspective, ensuring clarity and usability",
        "value": "Ensures solutions are user-friendly and meet actual user needs"
    }
}


default_worker_divisions = {
1: {
    "worker_name": "Data Researcher",
    "subtask": "Research and extract relevant information from available sources",
    "input_requirements": {
        "files": "Access to provided files and documents",
        "metadata": "Access to available metadata",
        "query": "Original user request"
    },
    "expected_outputs": {
        "research_findings": "Key information extracted from sources",
        "source_references": "List of sources used"
    },
    "dependencies": "None",
    "success_criteria": "Comprehensive information gathered from available sources"
},

2: {
    "worker_name": "Technical Analyzer",
    "subtask": "Analyze technical aspects and implementation considerations",
    "input_requirements": {
        "query": "Original user request",
        "tools": "Available tool specifications"
    },
    "expected_outputs": {
        "technical_analysis": "Technical considerations and requirements",
        "feasibility_assessment": "Assessment of technical feasibility"
    },
    "dependencies": "None",
    "success_criteria": "Clear technical analysis with implementation considerations"
},

3: {
    "worker_name": "Requirements Evaluator",
    "subtask": "Identify and evaluate core requirements and constraints",
    "input_requirements": {
        "query": "Original user request",
        "context": "Any provided context"
    },
    "expected_outputs": {
        "requirements_list": "List of identified requirements",
        "constraints": "Identified limitations or constraints"
    },
    "dependencies": "None",
    "success_criteria": "Comprehensive list of requirements and constraints"
},

4: {
    "worker_name": "Quality Assessor",
    "subtask": "Evaluate quality aspects and potential issues",
    "input_requirements": {
        "query": "Original user request",
        "context": "Available context"
    },
    "expected_outputs": {
        "quality_criteria": "Identified quality requirements",
        "risk_assessment": "Potential issues or concerns"
    },
    "dependencies": "None",
    "success_criteria": "Thorough quality and risk assessment"
},

5: {
    "worker_name": "Solution Architect",
    "subtask": "Design high-level solution approach",
    "input_requirements": {
        "query": "Original user request",
        "tools": "Available tool specifications"
    },
    "expected_outputs": {
        "solution_approach": "High-level solution design",
        "architecture_recommendations": "Key architectural decisions"
        },
        "dependencies": "None",
        "success_criteria": "Clear solution architecture that addresses the request"
    }
}
