# pvplot
Package for dynamic plotting of EPICS PVs (both CA and PVA) and [liteServer data objects](https://github.com/ASukhanov/liteServer).

## Examples
- Sliced array plot of EPICS Channel Access [testAsynPortDriverApp](https://epics.anl.gov/modules/soft/asyn/R4-38/asynDriver.html#testAsynPortDriverApp):<br>
`python -m pvplot -s0.01 -a'E:testAPD:scope1:' 'Waveform_RBV[1:500]'`
- Waveform from EPICS PVaccess [simScope](https://github.com/ASukhanov/p4pex):<br>
`python -m pvplot P:simScope1:Waveform_RBV`
- Time-series plot (stripchart) of analog inputs of a LabJack U3-HV instrument, served by liteLabjack:<br>
`python -m pvplot -a'L:localhost:dev1' 'tempU3 ADC_HV[0] ADC_HV[1] ADC_HV[2] ADC_HV[3] ADC_LV'`
- Fast correlation plot of a litePeakSimulator<br>
`python -m pvplot -s.01 -a'L:localhost:dev1' 'x,y'`
- Multiple docks. For example, to plot two scrolling plots in lower dock and a 
correlation plot in upper dock:<br>
`python -m pvplot -a'L:localhost:dev1:' -#0'yMax yMin' -#1'yMax,yMin'`
- To change properties of curves: right click on a plot and select 'DataSets Options'
