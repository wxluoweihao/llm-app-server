import axios from 'axios'
import { ICommonObject, INode, INodeData, INodeParams } from '../../../src/Interface'
import { getBaseClasses } from '../../../src'
import { Calculator } from 'langchain/tools/calculator'

class RemoteAgent_Tools implements INode {
    label: string
    name: string
    version: number
    description: string
    type: string
    icon: string
    category: string
    baseClasses: string[]
    inputs: INodeParams[]
    remoteUrl: String
    agentId: String

    constructor() {
        this.label = 'Agent Worker'
        this.name = 'AgentWorker'
        this.version = 1.0
        this.type = 'Tools'
        this.icon = 'agentworker.png'
        this.category = 'Agents'
        this.description = 'worker agent that accept connection from Remote Chat Agent'
        this.inputs = [
            {
                label: 'Remote chat agent name',
                name: 'remoteEndPointName',
                type: 'string',
                placeholder: '',
                optional: false
            },
            {
                label: 'Remote chat agent url',
                name: 'remoteEndPoint',
                type: 'string',
                placeholder: 'http://localhost:3001',
                optional: false
            }
        ]
        this.baseClasses = [this.type, ...getBaseClasses(Calculator)]
    }

    async init (nodeData: INodeData, _: string, options: ICommonObject): Promise<any> {
        this.remoteUrl = nodeData.inputs?.remoteEndPoint
        this.agentId = nodeData.inputs?.remoteEndPointName
        console.log('################## initilizing agent worker: ' + this.agentId + ', in session: ' + options.chatflowid)

        // send get post request
        const data = {
            sessionId: options.chatflowid,
            agent: {
                name: this.agentId,
                url: nodeData.inputs?.remoteEndPoint
            }
        }
        console.log('init, sending request: ' + JSON.stringify(data))
        return await axios
            .post('http://localhost:3000/api/v1/chat/session/addTool', data)
            .then(function (response) {
                console.log(JSON.stringify(response.data))
                return response.status
            })
            .catch(function (error) {
                console.log(error.toJSON())
            })
    }
}

module.exports = { nodeClass: RemoteAgent_Tools }
