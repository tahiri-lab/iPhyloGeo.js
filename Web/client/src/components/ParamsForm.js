import React from "react";
import { useState } from "react";
//import InputPrepare from "./InputPrepare";
import { useNavigate } from 'react-router-dom';
// import {Routes, Route, Link} from "react-router-dom";
// import ErrorComponent from './ErrorComponent';

function ParamsForm() {
    const navigate = useNavigate();
    const [form, setForm] = useState({ 
        bootStrap: '0', 
        rf: '100', 
        windowSize: '', 
        stepSize: '',
        alignmentAlgo:'muscle',
        phyloAlgo:'fasttree',
      });

    const handleSubmit = (e) => {
        e.preventDefault();
        if (form.windowSize === '0' || form.stepSize === '0'){
            alert("Please provide Window Size value and Step Size value greater than zero")
        } else {alert("Parameters Submitted");
                navigate('/aPhyloGeo',{replace:true});
                }
        setForm({bootStrap: '0', 
            rf: '100', 
            windowSize: '', 
            stepSize: '',
            alignmentAlgo:'muscle',
            phyloAlgo:'fasttree',});
        // alert('bootstrap' + form.bootStrap+'; '+ 'rf: '+form.rf+'; ' + 'windowSize: '+form.windowSize+'; '+'stepSize: '+form.stepSize+'; ');
        //alert(Object.keys(form).length);
        //alert(Object.values(form).every(x => x == null || x == ''));
        // alert(Object.values(form).some(x => x == null || x == ''));
        }


    return (
            <div className="page-body">
                <form onSubmit={handleSubmit}>
                <div className="row">
                    <div className="col">
                        <label htmlFor="bootstrap">Bootstrap threshold: {form.bootStrap} </label>
                        <input type="range" min="0" max="100" className="slider" id="bootstrap" 
                                value={form.bootStrap}
                                onChange = {e => {
                                    setForm({
                                        ...form,
                                        bootStrap: e.target.value
                                    });
                                }}></input>
                    </div>
                    <div className="col">
                        <label htmlFor="rf">RF distance: {form.rf} </label>
                        <input type="range" min="0" max="100" className="slider" id="rf" 
                            value={form.rf}
                            onChange = {e => {
                                setForm({
                                    ...form,
                                    rf: e.target.value
                                });
                            }}></input>
                    </div>
                </div>
                <br />
                <div className="row">
                    <div className="col">
                        <label htmlFor="windowSize">Window Size <sup style = {{color:'crimson'}}>*</sup> </label>
                        <input type="text" className="form-control" id="windowsize" placeholder="Please enter the window size value greater than 0 "
                            value={form.windowSize}
                            onChange = {e => {
                                setForm({
                                    ...form,
                                    windowSize: e.target.value
                                });
                            }}></input>
                    </div>
                    <div className="col">
                        <label htmlFor="stepSize">Step Size <sup style = {{color:'crimson'}}>*</sup> </label>
                        <input type="text" className="form-control" id="stepSize" placeholder="Please enter the step size value greater than 0"
                            value={form.stepSize}
                            onChange = {e => {
                                setForm({
                                    ...form,
                                    stepSize: e.target.value
                                });
                            }}></input>
                    </div>
                </div>
                <br />
                <div className="row">
                    <div className="col">
                        <label>Analytical Strategy in Alignment <sup style = {{color:'crimson'}}>*</sup> </label>
                        <select value={form.alignmentAlgo} className="custom-select my-1 mr-sm-2" onChange= {e => {
                                setForm({
                                    ...form,
                                    alignmentAlgo: e.target.value
                                });
                        }}> 
                            <option value="muscle">MUSCLE</option> 
                            <option value="omega">Clustal Omega</option> 
                        </select> 
                    </div>
                    <div className="col">
                        <label>Analytical Strategy in Phylogenetic Tree Construction <sup style = {{color:'crimson'}}>* </sup> </label>
                        <select value={form.phyloAlgo} className="custom-select my-1 mr-sm-2" onChange= {e => {
                                    setForm({
                                        ...form,
                                        phyloAlgo: e.target.value
                                    });
                            }}> 
                            <option value="fasttree">FastTree</option> 
                            <option value="raxml">RAxML-NG</option> 
                        </select> 
                    </div>
                </div>
                <br />
                
                {/* <Link to="/aPhyloGeo" type="submit" className="btn btn-primary" style={{marginRight:'60px'}}>Submit</Link> */}
                <button disabled = {Object.values(form).some(x => x === null || x === '')} type="submit" className="btn btn-primary" style={{marginRight:'60px'}}>Submit</button>
                <input className="btn btn-primary" type="reset" value="Reset"
                            onClick = {e => {
                                setForm({
                                    bootStrap: '0', 
                                    rf: '100', 
                                    windowSize: '', 
                                    stepSize: '',
                                    alignmentAlgo:'muscle',
                                    phyloAlgo:'fasttree',
                                });
                            }}></input>
               
            </form>
            {/* <InputPrepare form={form} /> */}
           
            
            </div>
        );
    };
    
    export default ParamsForm;