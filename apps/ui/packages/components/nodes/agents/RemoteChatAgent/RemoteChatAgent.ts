import axios from 'axios'
import { ICommonObject, INode, INodeData, INodeParams } from '../../../src/Interface'

class RemoteChatAgent_Agents implements INode {
    label: string
    name: string
    version: number
    description: string
    type: string
    icon: string
    category: string
    baseClasses: string[]
    inputs: INodeParams[]
    remoteUrl: string
    sessionId: string

    constructor() {
        this.label = 'Remote Chat Agent'
        this.name = 'remoteChatAgent'
        this.version = 1.0
        this.type = 'AgentExecutor'
        this.category = 'Agents'
        this.icon = 'remotechatagent.png'
        this.description = `A remote agent that route messages between other agents`
        this.baseClasses = [this.type]
        this.inputs = [
            {
                label: 'Remote chat agent url',
                name: 'remoteEndPoint',
                type: 'string',
                placeholder: 'http://localhost:3001',
                optional: true
            },
            {
                label: 'Allowed Tools',
                name: 'tools',
                type: 'Tool',
                list: true
            }
        ]
    }

    async init (nodeData: INodeData, _: string, options: ICommonObject): Promise<any> {
        console.log('################## arrive in remote chat ! ' + options.chatflowid)
        return await axios
            .post('http://localhost:3300/xxx', {
                sessionId: 'mikeeeeee'
            })
            .then(function (response) {
                console.log('post request answer: ' + JSON.stringify(response.data))
                return response.status
            })
            .catch(function (error) {
                console.log('post request error: ' + console.log(error.toJSON()))
            })
    }

    async run (nodeData: INodeData, input: string, options: ICommonObject): Promise<string> {
        const remoteChatAgentUrl = nodeData.inputs?.remoteEndPoint + '/api/v1/sendChatMsg'
        console.log('---------- ' + this.sessionId)
        const runRequest = {
            sessionId: options.chatflowid,
            message: input
        }
        console.log('init, sending request: ' + JSON.stringify(runRequest))
        return await axios
            .post(remoteChatAgentUrl, runRequest)
            .then(function (response) {
                console.log('post request answer: ' + JSON.stringify(response.data))
                return response.status
            })
            .catch(function (error) {
                console.log('post request error: ' + console.log(error.toJSON()))
            })
    }
}

module.exports = { nodeClass: RemoteChatAgent_Agents }
