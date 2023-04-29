import React from 'react';
import workflow from '../assets/images/workflow.png'

function IntroWorkflow(){
    const workfkowImg = <img src={workflow} alt="workflow" width="1000"/>;
    return workfkowImg
}

function Waiting(props) {
    return (
        <>
            <div>
                {/* <h2>bootStrap:  {props.form.bootStrap}</h2>
                <h2>rf:  {props.form.rf}</h2>
                <h2>windowSize:  {props.form.windowSize}</h2>
                <h2>stepSize:  {props.form.stepSize}</h2>
                <h2>alignmentAlgo:  {props.form.alignmentAlgo}</h2>
                <h2>phyloAlgo:  {props.form.phyloAlgo}</h2> */}
            </div>
            <div className="centerImg">
                <h2>Workflow</h2>
                <IntroWorkflow />
            </div>
        </>
        
    )
}

export default Waiting
