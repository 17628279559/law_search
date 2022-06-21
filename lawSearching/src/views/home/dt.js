import * as d3 from 'd3'

const dt = (
  odata,
  {
    id, //
    mapSize = 650,
    width = 1300,
    height = 900,
    color = ['#FFF8DC', '#BB2020'],
    frontText = '',
    endText = ''
  } = {}
) => {
  let dtdata = odata.data2
  const colors = d3.scaleLinear().domain([0, 9]).range(color)
  let data = odata.data1

  let svg = d3.select(id).append('svg').attr('width', width).attr('height', height).style('z-index', '98')
  let tooltip = d3.select(id).append('div').attr('class', 'tooltip').style('opacity', 0.0).style('z-index', '9999')
  let projection = d3
    .geoMercator()
    .center([104, 27])
    .scale(mapSize)
    .translate([width / 2, height / 2 + 60])
  let path = d3.geoPath().projection(projection)

  const china = svg.append('g')

  let province = china
    .selectAll('path') //选中china内的所有path标签
    .data(dtdata.features) //所用数据为geojson文件下的features内容
    .enter() //进入循环内部
    .append('path') //每一次循环新建一个path标签
    .attr('fill', (d, i) => colors(Math.log(data[d['properties']['name']]) / Math.log(4)))
    .attr('d', path) //对于每个path标签中的d标签用path绘制
    .attr('stroke', 'red') //path的颜色
    .attr('stroke-width', 0.3) //path的粗细
    .on('mouseover', (d, i) => {
      tooltip.style('opacity', 1.0).text(`${frontText}${i['properties']['name']}${data[i['properties']['name']]}${endText}`)
      d3.select(d.target).attr('fill', '#FFF8F8')
    })
    .on('mouseout', (d, i) => {
      tooltip.style('opacity', 0.0)
      d3.select(d.target).attr('fill', colors(Math.log(data[i['properties']['name']]) / Math.log(4)))
    })
    .on('mousemove', ev => {
      tooltip.style('left', ev.clientX + 10 + 'px').style('top', ev.clientY + 10 + 'px')
    })
}

export default dt
