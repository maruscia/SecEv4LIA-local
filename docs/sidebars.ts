import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';
/**
 * Creating a sidebar allows you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    'introduction',
    {
      type: 'category',
      label: 'Getting Started',
      className: 'sidebar-icon sidebar-icon-rocket',
      items: [
        'getting-started/installation',
        'getting-started/quick-start',
        'getting-started/attack-tutorial',
        'getting-started/datasets-tutorial',
      ],
    },
    {
      type: 'category',
      label: 'AI Risks Assessment',
      className: 'sidebar-icon sidebar-icon-shield-alert',
      link: {
        type: 'doc',
        id: 'risks/index',
      },
      items: [
        {
          type: 'category',
          label: 'Vulnerabilities',
          link: {
            type: 'doc',
            id: 'risks/risk-categories',
          },
          items: [
            'risks/vulnerabilities',
            'risks/vulnerabilities/prompt-injection',
            'risks/vulnerabilities/jailbreak',
            'risks/vulnerabilities/input-manipulation-attack',
            'risks/vulnerabilities/system-prompt-leakage',
            'risks/vulnerabilities/model-evasion',
            'risks/vulnerabilities/craft-adversarial-data',
            'risks/vulnerabilities/sensitive-information-disclosure',
            'risks/vulnerabilities/misinformation',
            'risks/vulnerabilities/excessive-agency',
            'risks/vulnerabilities/malicious-tool-invocation',
            'risks/vulnerabilities/credential-exposure',
            'risks/vulnerabilities/public-facing-application-exploitation',
            'risks/vulnerabilities/vector-embedding-weaknesses-exploit',
            {
              type: 'doc',
              id: 'risks/custom-vulnerabilities',
              label: 'Custom',
            },
          ],
        },
        {
          type: 'category',
          label: 'Threat Profiles',
          link: {
            type: 'doc',
            id: 'risks/threat-profiles',
          },
          items: [
            'risks/threat-profiles/prompt-injection',
            'risks/threat-profiles/jailbreak',
            'risks/threat-profiles/input-manipulation-attack',
            'risks/threat-profiles/system-prompt-leakage',
            'risks/threat-profiles/model-evasion',
            'risks/threat-profiles/craft-adversarial-data',
            'risks/threat-profiles/sensitive-information-disclosure',
            'risks/threat-profiles/misinformation',
            'risks/threat-profiles/excessive-agency',
            'risks/threat-profiles/malicious-tool-invocation',
            'risks/threat-profiles/credential-exposure',
            'risks/threat-profiles/public-facing-application-exploitation',
            'risks/threat-profiles/vector-embedding-weaknesses-exploit',
          ],
        },
        {
          type: 'category',
          label: 'Evaluation Campaigns',
          link: {
            type: 'doc',
            id: 'risks/evaluation-campaigns',
          },
          items: [
            'risks/evaluation-campaigns/quick-scan',
            'risks/evaluation-campaigns/comprehensive-audit',
            'risks/evaluation-campaigns/targeted-assessment',
            'risks/evaluation-campaigns/custom-campaigns',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Attacks',
      className: 'sidebar-icon sidebar-icon-sword',
      link: {
        type: 'doc',
        id: 'attacks/index',
      },
      items: [
        'attacks/advprefix',
        'attacks/autodan_turbo',
        'attacks/pair',
        'attacks/tap',
        'attacks/flipattack',
        'attacks/bon',
        'attacks/h4rm3l',
        'attacks/cipherchat',
        'attacks/pap',
        'attacks/baseline',
      ],
    },
    {
      type: 'category',
      label: 'Datasets',
      className: 'sidebar-icon sidebar-icon-database',
      link: {
        type: 'doc',
        id: 'datasets/index',
      },
      items: [
        'datasets/presets',
        'datasets/huggingface',
        'datasets/file',
        'datasets/custom-providers',
      ],
    },
    {
      type: 'category',
      label: 'Agents',
      className: 'sidebar-icon sidebar-icon-cpu',
      link: {
        type: 'doc',
        id: 'agents/index',
      },
      items: [
        {
          type: 'doc',
          id: 'agents/ollama',
          label: 'Ollama',
        },
        {
          type: 'doc',
          id: 'agents/openai-sdk',
          label: 'OpenAI SDK',
        },
        {
          type: 'doc',
          id: 'agents/google-adk',
          label: 'Google ADK',
        },
      ],
    },
    {
      type: 'category',
      label: 'CLI Reference',
      className: 'sidebar-icon sidebar-icon-terminal',
      items: [
        'cli/overview',
        'cli/initialization',
        'cli/config',
        'cli/attack',
        'cli/examples-ollama',
        'cli/results',
      ],
    },
    {
      type: 'category',
      label: 'API Reference',
      className: 'sidebar-icon sidebar-icon-code',
      link: {
        type: 'doc',
        id: 'api-index',
      },
      items: [
        'secev4lia/agent',
        'secev4lia/errors',
        'secev4lia/logger',
        'secev4lia/utils',
        {
          type: 'category',
          label: 'Router',
          items: [
            'secev4lia/router/router',
            'secev4lia/router/types',
            {
              type: 'category',
              label: 'Adapters',
              items: [
                'secev4lia/router/adapters/base',
                'secev4lia/router/adapters/openai',
                'secev4lia/router/adapters/ollama',
                'secev4lia/router/adapters/litellm',
                'secev4lia/router/adapters/google_adk',
              ],
            },
            {
              type: 'category',
              label: 'Tracking',
              items: [
                'secev4lia/router/tracking/tracker',
                'secev4lia/router/tracking/coordinator',
                'secev4lia/router/tracking/context',
                'secev4lia/router/tracking/step',
                'secev4lia/router/tracking/decorators',
                'secev4lia/router/tracking/utils',
              ],
            },
          ],
        },
        {
          type: 'category',
          label: 'Attacks',
          items: [
            'secev4lia/attacks/base',
            'secev4lia/attacks/orchestrator',
            'secev4lia/attacks/registry',
            {
              type: 'category',
              label: 'Evaluator',
              items: [
                'secev4lia/attacks/evaluator/base',
                'secev4lia/attacks/evaluator/evaluation_step',
                'secev4lia/attacks/evaluator/judge_evaluators',
                'secev4lia/attacks/evaluator/pattern_evaluators',
                'secev4lia/attacks/evaluator/metrics',
              ],
            },
            {
              type: 'category',
              label: 'Techniques',
              items: [
                'secev4lia/attacks/techniques/base',
                'secev4lia/attacks/techniques/advprefix/attack',
                'secev4lia/attacks/techniques/pair/attack',
                'secev4lia/attacks/techniques/tap/attack',
                'secev4lia/attacks/techniques/bon/attack',
                'secev4lia/attacks/techniques/flipattack/attack',
                'secev4lia/attacks/techniques/autodan_turbo/attack',
                'secev4lia/attacks/techniques/baseline/attack',
              ],
            },
          ],
        },
        {
          type: 'category',
          label: 'Datasets',
          items: [
            'secev4lia/datasets/base',
            'secev4lia/datasets/presets',
            'secev4lia/datasets/registry',
            'secev4lia/datasets/providers/file',
            'secev4lia/datasets/providers/huggingface',
          ],
        },
        {
          type: 'category',
          label: 'Risks',
          items: [
            'secev4lia/risks/base',
            'secev4lia/risks/profile_types',
            'secev4lia/risks/profile_helpers',
            'secev4lia/risks/registry',
            'secev4lia/risks/utils',
          ],
        },
        {
          type: 'category',
          label: 'Server',
          items: [
            'secev4lia/server/client',
            'secev4lia/server/types',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Security & Ethics',
      className: 'sidebar-icon sidebar-icon-lock',
      items: [
        'security/responsible-disclosure',
        'security/ethical-guidelines',
      ],
    },
    {
      type: 'category',
      label: 'Advanced Usage',
      className: 'sidebar-icon sidebar-icon-settings',
      items: [
        'tutorial-extras/manage-docs-versions',
      ],
    },
  ]
};

export default sidebars;
